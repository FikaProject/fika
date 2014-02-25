from betahaus.viewcomponent import view_action

from fika.models.interfaces import ICourseModule
from fika import security
from fika import FikaTSF as _


@view_action('actions', 'view', permission = security.VIEW, title=_(u"View"),
             icon = 'eye', view_name = '')
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
    return """<li class="%(active_cls)s"><a href="%(url)s"><span class="glyphicon glyphicon-%(icon)s">%(title)s</span></a></li>""" % \
        {'icon': va.kwargs['icon'], 'title': va.title, 'active_cls': active_cls, 'url': url}
