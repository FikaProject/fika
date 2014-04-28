from zope.interface import implementer

from .interfaces import ICourseModules
from .base import FikaBaseFolder
from fika import FikaTSF as _


@implementer(ICourseModules)
class CourseModules(FikaBaseFolder):
    title = type_title = _(u"Course modules")
    type_name = u"CourseModules"
    addable_to = ()
    #add_permission = "Add %s" % type_name FIXME: Needed?

def includeme(config):
    config.add_content_factory(CourseModules)
