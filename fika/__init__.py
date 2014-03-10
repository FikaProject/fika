from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
from pyramid.i18n import TranslationStringFactory
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy

FikaTSF = TranslationStringFactory('fika')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    from fika.models.security_mixin import groupfinder
    authn_policy = AuthTktAuthenticationPolicy(secret = read_salt(settings),
                                               callback = groupfinder,
                                               hashalg = 'sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(root_factory = root_factory,
                          settings = settings,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy,)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform', 'deform:static')
    config.include('pyramid_beaker')
    config.include('pyramid_zodbconn')
    config.include('pyramid_tm')
    config.include('pyramid_deform')
    config.include('deform_bootstrap')
    config.include('js.deform')
    config.include('js.deform_bootstrap')
    config.scan('betahaus.pyracont.fields.password')
    config.include('fika')
    config.add_translation_dirs('fika:locale/')
    config.hook_zca()
    return config.make_wsgi_app()

def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())

def appmaker(zodb_root):
    try:
        return zodb_root['app_root']
    except KeyError:
        zodb_root['app_root'] = populate_database()
        import transaction
        transaction.commit()
        return zodb_root['app_root']

def populate_database():
    from fika.models.site import SiteRoot
    from fika.models.user import User
    from fika.models.users import Users
    from fika.models.courses import Courses
    from fika.models.course_modules import CourseModules
    from fika.security import ROLE_ADMIN
    from fika.security import get_security
    from fika.models.interfaces import IFlashMessages
    from pyramid.threadlocal import get_current_request
    site = SiteRoot()
    site['users'] = Users()
    admin = User(password = 'admin', email = 'admin@fika.com')
    site['users'][admin.uid] = admin
    sec = get_security(site)
    sec.add_groups(admin.userid, [ROLE_ADMIN])
    site['courses'] = Courses()
    site['course_modules'] = CourseModules()
    request = get_current_request()
    fm = request.registry.queryAdapter(request, IFlashMessages)
    if fm: #To avoid having to deal with this during tests
        _ = FikaTSF #_ enables translations to be found
        msg = _(u"site_populated_info",
                default = u"Since this is the first time you're using Fika, the site has been populated "
                    u"with a default user. You may login with <b>admin@localhst</b> and password <b>admin</b>. ")
        fm.add(msg, auto_destruct = False)
    return site

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


def includeme(config):
    config.include('fika.models')
    config.include('fika.schemas')
    config.include('fika.views')
