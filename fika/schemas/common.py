from StringIO import StringIO

import colander
from pyramid.traversal import find_root
from betahaus.pyracont.decorators import schema_factory

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


@schema_factory('DeleteSchema')
class DeleteSchema(colander.Schema):
    pass


class FileUploadTempStore(object):
    """
    A temporary storage for file file uploads

    File uploads are stored in the session so that you don't need
    to upload your file again if validation of another schema node
    fails.
    """

    def __init__(self, request):
        self.session = request.session

    def keys(self):
        return [k for k in self.session.keys() if not k.startswith('_')]

    def get(self, key, default = None):
        return key in self.keys() and self.session[key] or default

    def __setitem__(self, name, value):
        value = value.copy()
        fp = value.pop('fp')
        value['file_contents'] = fp.read()
        fp.seek(0)
        self.session[name] = value

    def __getitem__(self, name):
        #import pdb;pdb.set_trace()
        value = self.session[name].copy()
        value['fp'] = StringIO(value.pop('file_contents'))
        return value

    def __delitem__(self, name):
        del self.session[name]

    def preview_url(self, name):
        return None
