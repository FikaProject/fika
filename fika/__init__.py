from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
from pyramid.i18n import TranslationStringFactory

FikaTSF = TranslationStringFactory('fika')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory = root_factory, settings = settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform', 'deform:static')
    config.include('deform_bootstrap')
    config.include('js.deform')
    config.include('js.deform_bootstrap')
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

def include_defaults(config):
    config.include('fika.models')
    config.include('fika.views')
