

def includeme(config):
    config.scan()
    config.include('fika.models.security_mixin')
    config.include('fika.models.flash_messages')
