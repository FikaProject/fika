# import colander
# import deform
# from js.deform import auto_need
# from js.jqueryui import jqueryui
# from betahaus.pyracont.factories import createSchema
# from pyramid.view import view_config
# from pyramid.httpexceptions import HTTPFound
# 
# from fika import security
# from fika.views.base import BaseView
# from fika.models.interfaces import ISiteRoot
# from fika.models.interfaces import ISecurity
# 
# 
# class PermissionsView(BaseView):
#     
#     @view_config(context = ISiteRoot, name = "permissions", renderer = "fika:templates/form.pt",
#                  permission = security.MANAGE_SERVER)
#     def edit(self):
#         schema = createSchema('PermissionsSchema')
#         schema = schema.bind(context = self.context, request = self.request, view = self)
#         form = deform.Form(schema, buttons = ('save', 'cancel'))
#         auto_need(form)
#         sec = self.request.registry.getAdapter(self.context, ISecurity)
#         if self.request.method == 'POST':
#             if 'save' in self.request.POST:
#                 controls = self.request.POST.items()
#                 try:
#                     appstruct = form.validate(controls)
#                 except deform.ValidationFailure, e:
#                     self.response['form'] = e.render()
#                     return self.response
#                 sec.set_security(appstruct['userids_and_groups'])
#             return HTTPFound(location = self.request.resource_url(self.context))
#         appstruct = {}
#         appstruct['userids_and_groups'] = sec.get_security()
#         self.response['form'] = form.render(appstruct = appstruct)
#         return self.response
