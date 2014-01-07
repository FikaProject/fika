from pyramid.config import Configurator
from pyramid_zodbconn import get_connection


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory = root_factory, settings = settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform', 'deform:static')
    config.include(include_defaults)
    config.scan()
    config.hook_zca()
    return config.make_wsgi_app()

def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        from fika.models.site import SiteRoot
        app_root = SiteRoot()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']

def include_defaults(config):
    config.include('fika.views')
