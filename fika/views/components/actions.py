from betahaus.viewcomponent import view_action
from pyramid.renderers import render

from fika.models.interfaces import ICourseModule
from fika import security
from fika import FikaTSF as _

# permission set to edit on view action, so that the view button does not show up unless you have the other permissions as well.
@view_action('actions', 'view', permission = security.EDIT, title=_(u"View"),
             icon = 'eye-open', view_name = '') 
@view_action('actions', 'edit', permission = security.EDIT, title=_(u"Edit"),
             icon = 'edit', view_name = 'edit', schema_required = 'edit')
@view_action('actions', 'delete', permission = security.DELETE, title=_(u"Delete"),
             icon = 'remove-circle', view_name = 'delete', schema_required = 'delete')
@view_action('actions', 'order', permission = security.EDIT, title=_(u"Order"),
             icon = 'sort-by-attributes', view_name = 'order', interface = ICourseModule)
def generic_action_menu(context, request, va, **kw):
    if 'schema_required' in va.kwargs and context.schemas.get(va.kwargs['schema_required'], None) is None:
        return
    active_cls = va.kwargs['view_name'] == request.view_name and 'active' or ''
    url = request.resource_url(context, va.kwargs['view_name'])
    return """<li class="%(active_cls)s"><a href="%(url)s"><span class="glyphicon glyphicon-%(icon)s"></span> %(title)s</a></li>""" % \
        {'icon': va.kwargs['icon'], 'title': va.title, 'active_cls': active_cls, 'url': url}

@view_action('actions', 'add', priority = 1, title = _(u"Add"))
def add_action_menu(context, request, va, **kw):
    view = kw['view']
    if not view.addable_types:
        return
    response = {'view': view, 'context': context, 'va': va}
    return render("fika:templates/add_tab.pt", response, request = request)
