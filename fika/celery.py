from __future__ import absolute_import

from celery import Celery


#FIXME: Configurable

app = Celery('fika',
             broker='sqla+sqlite:///var/celerydb.sqlite',
             include=['fika.tasks'])

if __name__ == '__main__':
    app.conf.update(
        CELERY_REDIRECT_STDOUTS = True,
        CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO',
        CELERYD_MAX_TASKS_PER_CHILD = 1,
    )
    app.start()
