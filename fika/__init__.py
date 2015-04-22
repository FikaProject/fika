from pyramid.i18n import TranslationStringFactory

_ = FikaTSF = TranslationStringFactory('fika')
PERM_SHOW_CONTROLS = 'perm:Show controls'


def includeme(config):
    config.commit()
    config.include('fika.populator')
    config.include('fika.models')
    config.include('fika.schemas')
    config.include('fika.fanstatic')
    config.include('fika.views')
    config.include('fika.subscribers')
    config.add_translation_dirs('fika:locale/')
    config.override_asset(to_override='arche:templates/master.pt',override_with='fika:templates/overrides/master.pt')
    config.override_asset(to_override='arche:templates/content/basic.pt',override_with='fika:templates/overrides/content/basic.pt')
    config.override_asset(to_override='arche_video:templates/video.pt',override_with='fika:templates/overrides/video.pt')
    from arche.security import get_acl_registry
    from arche.utils import get_content_factories
    from arche.security import ROLE_ADMIN
    from arche.security import ROLE_EDITOR
    acl_reg = get_acl_registry(config.registry)
    factories = get_content_factories(config.registry)
    add_perms = []
    for factory in factories.values():
        if hasattr(factory, 'add_permission'):
            add_perms.append(factory.add_permission)
    #acl_reg.default.add(ROLE_ADMIN, add_perms)
    acl_reg['public'].add(ROLE_ADMIN, add_perms)
    
    acl_reg['public'].add(ROLE_EDITOR, PERM_SHOW_CONTROLS)
    acl_reg['User'].add(ROLE_EDITOR, PERM_SHOW_CONTROLS)
    
