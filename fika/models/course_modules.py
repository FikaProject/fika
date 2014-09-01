from zope.interface import implementer

from .interfaces import ICourseModules
from .base import FikaBaseFolder
from fika import FikaTSF as _


@implementer(ICourseModules)
class CourseModules(FikaBaseFolder):
    title = type_title = _(u"Course modules")
    type_name = u"CourseModules"
    is_permanent = True
    addable_to = ()


def includeme(config):
    config.add_content_factory(CourseModules)
