

def includeme(config):
    config.include('.content')
    config.include('.my_courses')
    config.include('.courses')
    config.include('.pdf')
    config.scan('fika.views')
