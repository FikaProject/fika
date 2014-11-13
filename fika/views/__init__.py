

def includeme(config):
    config.include('.content')
    config.include('.my_courses')
    config.include('.courses')
    config.include('.pdf')
    config.include('.assessment_view')
    config.scan('fika.views')
