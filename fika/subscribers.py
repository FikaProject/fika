from arche_video.interfaces import INewVideo

from fika.tasks import create_video_task_structure


def convert_video_subscriber(event):
    print "SUBSCRIBER FIRED"
    create_video_task_structure(event.video)


def includeme(config):
    print "Not including video subscribers right now"
    #config.add_subscriber(convert_video_subscriber, INewVideo)
