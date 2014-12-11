from __future__ import absolute_import
from subprocess import call
from tempfile import NamedTemporaryFile
from tempfile import mktemp
import mimetypes
import os

from arche.api import File
from arche.interfaces import IBlobs
from arche.interfaces import IFile
from arche.utils import generate_slug
from celery import chain
from pyramid.paster import bootstrap
from pyramid.traversal import resource_path, find_resource
import transaction

from fika.celery import app

#FIXME: Very early testing stage - don't use this code for anything real yet.


def _env():
    #FIXME: Make this configurable, or create a proper worker config
    return bootstrap('etc/development.ini')


#from fika.tasks import *
#create_video_task_structure(root['sd']['movie-mp4'])

def create_video_task_structure(obj):
    """ The video conversion consists of several different steps.
        They need to be linked together for this to work. Something like.
        
        blob to file > convert file > create db file object (if successful do cleanup)
    """
    parent_path = resource_path(obj.__parent__)
    obj_path = resource_path(obj)
    types = ['.mkv', '.avi'] #FIXME: Settings, formats etc...
    results = []
    for mtype in types:
        task_c = chain(blob_to_tmp_file.s(obj_path), convert_file.s(mtype), tmp_to_blob.s(parent_path, obj_path))
        results.append(task_c())
    return results

@app.task
def blob_to_tmp_file(obj_path):
    env = _env()
    obj = find_resource(env['root'], obj_path)
    assert IFile.providedBy(obj), "IFile not provided by %r" % obj
    orig_suffix = ".%s" % IBlobs(obj)['file'].filename.split('.')[-1]
    with IBlobs(obj)['file'].blob.open() as f:
        with NamedTemporaryFile(mode = 'wb', delete = False, suffix = orig_suffix) as video_file:
            for x in f:
                video_file.write(x)
            video_file_name = video_file.name
    env['closer']()
    print "new temp video file to convert: %s" % video_file_name
    return video_file_name

@app.task
def convert_file(filename, suffix):
    assert suffix.startswith('.')
    output_filename = mktemp(suffix = suffix)
    print output_filename
    if call(['ffmpeg', '-i', filename, output_filename]) == 0:
        return filename, output_filename
    os.remove(output_filename)
    raise Exception("Badness")

@app.task
def tmp_to_blob(filenames, parent_path, obj_path):
    original = filenames[0]
    filename = filenames[1]
    env = _env()
    root = env['root']
    parent = find_resource(root, parent_path)
    orig_obj = find_resource(root, obj_path)
    appstruct = {}
    mimetype = mimetypes.guess_type(filename)[0]
    if not mimetype:
        mimetype = "video/%s" % filename.split('.')[-1]
    obj_filename = "%s.%s" % ("".join(orig_obj.filename.split('.')[:-1]), filename.split('.')[-1])
    appstruct['file_data'] = {'filename': obj_filename,
                              'mimetype': mimetype,
                              'size': os.path.getsize(filename)}
    with open(filename, 'rb') as f:
        appstruct['file_data']['fp'] = f
        obj = File(**appstruct)
    name = generate_slug(parent, obj.filename)
    parent[name] = obj
    transaction.commit()
    env['closer']()
    os.remove(original)
    os.remove(filename)
