

def includeme(config):
    config.include('.auth')
    config.include('.content')
    config.include('.my_courses')
    config.include('.courses')
    config.include('.pdf')
    config.include('.assessment')
    config.scan('fika.views')
