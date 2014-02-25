

def includeme(config):
    config.include('fika.models.security_mixin')
    config.include('fika.models.flash_messages')
    config.scan('fika.models')
