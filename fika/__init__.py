from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
from pyramid.i18n import TranslationStringFactory
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy

FikaTSF = TranslationStringFactory('fika')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    authn_policy = AuthTktAuthenticationPolicy(secret = read_salt(settings),
                                               hashalg = 'sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(root_factory = root_factory,
                          settings = settings,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy,)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform', 'deform:static')
    config.include('deform_bootstrap')
    config.include('js.deform')
    config.include('js.deform_bootstrap')
    config.scan('betahaus.pyracont.fields.password')
    config.include(include_defaults)
    config.scan()
    config.hook_zca()
    return config.make_wsgi_app()

def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())

def appmaker(zodb_root):
    try:
        return zodb_root['app_root']
    except KeyError:
        from fika.models.site import SiteRoot
        from fika.models.users import Users
        from fika.models.courses import Courses
        from fika.models.course_modules import CourseModules
        site = SiteRoot()
        site['users'] = Users()
        site['courses'] = Courses()
        site['course_modules'] = CourseModules()
        zodb_root['app_root'] = site
        import transaction
        transaction.commit()
        return zodb_root['app_root']

def read_salt(settings):
    from uuid import uuid4
    from os.path import isfile
    filename = settings.get('salt_file', None)
    if filename is None:
        print "\nUsing random salt which means that all users must reauthenticate on restart."
        print "Please specify a salt file by adding the parameter:\n"
        print "salt_file = <path to file>\n"
        print "in paster ini config and add the salt as the sole contents of the file.\n"
        return str(uuid4())
    if not isfile(filename):
        print "\nCan't find salt file specified in paster ini. Trying to create one..."
        f = open(filename, 'w')
        salt = str(uuid4())
        f.write(salt)
        f.close()
        print "Wrote new salt in: %s" % filename
        return salt
    else:
        f = open(filename, 'r')
        salt = f.read()
        if not salt:
            raise ValueError("Salt file is empty - it needs to contain at least some text. File: %s" % filename)
        f.close()
        return salt


def include_defaults(config):
    config.include('fika.models')
    config.include('fika.views')
