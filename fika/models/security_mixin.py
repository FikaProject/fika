from BTrees.OOBTree import OOBTree
from pyramid.location import lineage
from zope.interface import implementer
from zope.component import adapter
from zope.interface.interfaces import ComponentLookupError
#from zope.component.event import objectEventNotify
from fika.models.interfaces import ISecurityAware

from fika.models.interfaces import ISecurity
from fika import security


#NON_INHERITED_GROUPS = ('role:Owner',)

ROLES_NAMESPACE = 'role:'
GROUPS_NAMESPACE = 'group:'
NAMESPACES = (ROLES_NAMESPACE, GROUPS_NAMESPACE, )


@adapter(ISecurityAware)
@implementer(ISecurity)
class Security(object):
    """
        All methods are documented in the interface of this class.
    """

    def __init__(self, context):
        self.context = context
        try:
            self._groups = self.context._groups
        except AttributeError:
            self.context._groups = OOBTree()
            self._groups = self.context._groups            
    
    def get_groups(self, principal):
        groups = set()
        for location in lineage(self.context):
            try:
                location_groups = location._groups
            except AttributeError:
                continue
            try:
                if self is location:
                    groups.update(location_groups[principal])
                else:
                    groups.update([x for x in location_groups[principal]])
            except KeyError:
                continue
        return tuple(groups)

    def add_groups(self, principal, groups, event = True):
        groups = set(groups)
        groups.update(self.get_groups(principal))
        #Delegate check and set to set_groups
        self.set_groups(principal, groups, event = event)

    def del_groups(self, principal, groups, event = True):
        if isinstance(groups, basestring):
            groups = set([groups])
        else:
            groups = set(groups)
        current = set(self.get_groups(principal))
        new_groups = current - groups
        #Delegate check and set to set_groups
        self.set_groups(principal, new_groups, event = event)

    def set_groups(self, principal, groups, event = True):
        changed = False
        if not groups:
            if principal in self._groups:
                del self._groups[principal]
                changed = True
        else:
            if groups != set(self.get_groups(principal)):
                self._groups[principal] = tuple(groups)
                changed = True
        if changed and event:
            self._notify()

    def get_security(self):
        userids_and_groups = []
        for userid in self._groups:
            userids_and_groups.append({'userid': userid,
                                       'groups': self.get_groups(userid)})
        return tuple(userids_and_groups)

    def set_security(self, value, event = True):
        submitted_userids = [x['userid'] for x in value]
        current_userids = self._groups.keys()
        for userid in current_userids:
            if userid not in submitted_userids:
                del self._groups[userid]

        for item in value:
            self.set_groups(item['userid'], item['groups'], event = False)
        if event:
            self._notify()

    def list_all_groups(self):
        groups = set()
        [groups.update(x) for x in self._groups.values()]
        return groups

    def _notify(self):
        pass
        #Only update specific index?
        #objectEventNotify(ObjectUpdatedEvent(self, metadata=True))


def groupfinder(name, request):
    try:
        context = request.context
        sec = request.registry.getAdapter(context, ISecurity)
        return sec.get_groups(name)
    except (AttributeError, ComponentLookupError): # pragma : no cover
        sec = Security(context)
        return sec.get_groups(name)


def includeme(config):
    config.registry.registerAdapter(Security)
