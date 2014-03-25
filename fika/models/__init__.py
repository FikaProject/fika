

def includeme(config):
    config.include('fika.models.security_mixin')
    config.include('fika.models.flash_messages')
    config.include('fika.models.catalog')
    config.scan('fika.models')
