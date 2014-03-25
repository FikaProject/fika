from pyramid.traversal import find_root
from pyramid.traversal import find_resource
from pyramid.traversal import resource_path

from repoze.catalog.indexes.field import CatalogFieldIndex
#from repoze.catalog.indexes.keyword import CatalogKeywordIndex
#from repoze.catalog.indexes.path import CatalogPathIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from zope.index.text.lexicon import CaseNormalizer
from zope.index.text.lexicon import Lexicon
from zope.index.text.lexicon import Splitter

from fika.models.interfaces import ICatalogable
from fika.models.interfaces import ISiteRoot
from fika.models.interfaces import IBaseFolder
from fika.interfaces import IObjectWillBeRemovedEvent
from fika.interfaces import IObjectAddedEvent
from fika.interfaces import IObjectUpdatedEvent


#FIXME: IObjectUpdatedEvent only fires on things that are from betahaus.pyracont
#File-objects aren,t so we might need to fire something here as well.

default_searchable_text_fields = ['title',
                                  'description',
                                  'body',
                                  'name',
                                  'email']


def update_indexes(catalog, reindex=True):
    """ Add or remove indexes. If reindex is True, also reindex all content if
        an index has been added or removed.
        Will return a set of indexes changed regardless.
    """
    lexicon = Lexicon(Splitter(), CaseNormalizer())
    
    indexes = {
        'title': CatalogFieldIndex(get_title),
        'sortable_title': CatalogFieldIndex(get_sortable_title),
        'searchable_text': CatalogTextIndex(get_searchable_text, lexicon = lexicon),
        'content_type': CatalogFieldIndex(get_content_type),
    }
    
    changed_indexes = set()
    
    # remove indexes
    for name in catalog.keys():
        if name not in indexes:
            del catalog[name]  

    # add indexes
    for name, index in indexes.iteritems():
        if name not in catalog:
            catalog[name] = index
            if reindex:
                changed_indexes.add(name)

    if reindex:
        reindex_indexes(catalog)

    return changed_indexes

def reindex_indexes(catalog):
    """ Warning! This will only update things that already are in the catalog! """
    root = find_root(catalog)
    for path in catalog.document_map.address_to_docid.keys():
        obj = find_resource(root, path)
        if ICatalogable.providedBy(obj):
            reindex_object(catalog, obj)

def index_object(catalog, obj):
    """ Index an object. """
    if not ICatalogable.providedBy(obj):
        return
    #Check if object already exists
    if catalog.document_map.docid_for_address(resource_path(obj)) is not None:
        reindex_object(catalog, obj)
        return
    obj_id = catalog.document_map.add(resource_path(obj))
    catalog.index_doc(obj_id, obj)

def reindex_object(catalog, obj, indexes = ()):
    """ Reindex an object.
        If indexes are specified, only reindex those indexes.
    """
    if not ICatalogable.providedBy(obj):
        return
    obj_id = catalog.document_map.docid_for_address(resource_path(obj))
    if obj_id is None:
        #This is a special case when an object that isn't indexed tries to be reindexed
        #Note that indexes parameter is ignored in that case
        index_object(catalog, obj) #Do reindex instead
        return
    if not indexes:
        catalog.reindex_doc(obj_id, obj)
    else:
        for index in indexes:
            catalog[index].reindex_doc(obj_id, obj)

def unindex_object(catalog, obj):
    """ Remove an index. """
    obj_id = catalog.document_map.docid_for_address(resource_path(obj))
    if obj_id is None:
        return
    catalog.unindex_doc(obj_id)
    catalog.document_map.remove_address(resource_path(obj))

#Indexes
def get_title(obj, default):
    """ Return objects title. """
    if IBaseFolder.providedBy(obj):
        return obj.get_field_value('title', default)
    return getattr(obj, 'title', default)

def get_sortable_title(obj, default):
    """ Sortable title is a lowercased version of the title. """
    if IBaseFolder.providedBy(obj):
        title = obj.get_field_value('title', default)
    else:
        title = getattr(obj, 'title', default)
    if title is default:
        return default
    return title.lower()

def get_searchable_text(obj, default):
    if IBaseFolder.providedBy(obj):
        output = u""
        for field_name in default_searchable_text_fields:
            text = obj.get_field_value(field_name, None)
            if isinstance(text, basestring):
                output += "%s " % text
        output = output.strip()
        if output:
            return output
    else:
        title = getattr(obj, 'title', default)
        if title is not default:
            return title
    return default

def get_content_type(obj, default):
    return obj.__class__.__name__

#Subscribers
def object_added(obj, event):
    root = find_root(obj)
    index_object(root.catalog, obj)

def object_updated(obj, event):
    root = find_root(obj)
    if ISiteRoot.providedBy(root):
        reindex_object(root.catalog, obj)

def object_removed(obj, event):
    root = find_root(obj)
    unindex_object(root.catalog, obj)

def includeme(config):
    config.add_subscriber(object_added, [ICatalogable, IObjectAddedEvent])
    config.add_subscriber(object_updated, [ICatalogable, IObjectUpdatedEvent])
    config.add_subscriber(object_removed, [ICatalogable, IObjectWillBeRemovedEvent])

