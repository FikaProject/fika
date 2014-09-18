

def includeme(config):
    config.include('.course_modules')
    config.include('.courses')
    config.include('.my_courses')
    config.include('.image_slideshow')
    config.include('.segment')
    config.scan('fika.views')
