from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import remember
import deform

from arche import _
from arche import security
from arche.interfaces import IRoot
from arche.views.auth import LoginForm


class FikaLoginForm(LoginForm):
    type_name = u'Auth'
    schema_name = 'login'
    title = _(u"Login")
    use_ajax = True
    formid = 'login-form'

    @property
    def buttons(self):
        return (deform.Button('login', title = _(u"Login"), css_class = 'btn btn-primary'),
                deform.Button('recover', title = _(u"Recover password"), css_class = 'btn btn'),)

    def recover_success(self, appstruct):
        return self.relocate_response(self.request.resource_url(self.root, 'recover_password'))
        
    recover_failure = recover_success

    def login_success(self, appstruct):
        email_or_userid = appstruct['email_or_userid']
        if '@' in email_or_userid:
            user = self.context['users'].get_user_by_email(email_or_userid)
        else:
            user = self.context['users'].get(email_or_userid, None)
        if user is None:
            raise HTTPForbidden("Something went wrong during login. No user profile found.")
        headers = remember(self.request, user.userid)
        url  = appstruct.pop('came_from', None)
        return self.relocate_response(url, headers = headers)


def includeme(config):
    config.add_view(FikaLoginForm,
                    context = IRoot,
                    name = 'login',
                    permission = security.NO_PERMISSION_REQUIRED,
                    renderer = 'fika:templates/loginform.pt')