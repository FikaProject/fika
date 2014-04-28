

def includeme(config):
    config.include('.course')
    config.include('.courses')
    config.include('.course_module')
    config.include('.course_modules')
    config.include('.module_segment')
    config.include('.user')

  #  config.include('fika.models.security_mixin')
  #  config.include('fika.models.flash_messages')
 #   config.include('fika.models.catalog')
   # config.scan('fika.models')
