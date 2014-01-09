import colander
from pyramid.traversal import find_root

from fika import FikaTSF as _


class NoDuplicates(object):
    """ Validator which succeeds if the iterable passed doesn't have duplicates. """

    def __call__(self, node, value):
        pool = set()
        for v in value:
            pool.add(v)
        if len(pool) != len(value):
            err = _("Must only contain unique values")
            raise colander.Invalid(node, err)

@colander.deferred
def deferred_login_password_validator(form, kw):
    context = kw['context']
    root = find_root(context)
    return LoginPasswordValidator(root)


class LoginPasswordValidator(object):
    """ Validate a password during login. context must be site root."""
    
    def __init__(self, context):
        self.context = context
        
    def __call__(self, form, value):
        exc = colander.Invalid(form, u"Login invalid") #Raised if trouble
        password = value['password']
        user = self.context['users'].get_user_by_email(value['email'])
        if not user:
            exc['email'] = _("Invalid email")
            raise exc
        #Validate password
        pw_field = user.get_custom_field('password')
        if not pw_field.check_input(password):
            exc['password'] = _(u"Wrong password. Remember that passwords are case sensitive.")
            raise exc
