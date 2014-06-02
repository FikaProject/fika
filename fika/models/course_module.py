from zope.interface import implementer

from .base import FikaBaseFolder
from .interfaces import ICourseModule
from fika import FikaTSF as _


@implementer(ICourseModule)
class CourseModule(FikaBaseFolder):
    type_title = _(u"Course module")
    type_name = u"CourseModule"
    add_permission = "Add %s" % type_name


def includeme(config):
    config.add_content_factory(CourseModule)
    config.add_addable_content("CourseModule", "CourseModules")
