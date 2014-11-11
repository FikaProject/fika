

def includeme(config):
    config.include('.courses')
    config.include('.my_courses')
    config.include('.image_slideshow')
    config.include('.video')
    config.include('.segment')
    config.include('.pdf')
    config.scan('fika.views')
