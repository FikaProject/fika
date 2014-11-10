

def includeme(config):
    config.include('.content')
    config.include('.my_courses')
    config.include('.courses')
    config.include('.pdf')
    config.include('.image_slideshow')
    config.include('.video')
    config.include('.segment')
    config.include('.assessment_view')
    config.scan('fika.views')
