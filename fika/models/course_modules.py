from arche.api import LocalRolesMixin
from zope.interface import implementer

from .interfaces import ICourseModules
from .base import FikaBaseFolder
from fika import FikaTSF as _

#FIXME Warning will be deleted!

@implementer(ICourseModules)
class CourseModules(FikaBaseFolder, LocalRolesMixin):
    title = type_title = _(u"Course modules")
    type_name = u"CourseModules"


def includeme(config):
    config.add_content_factory(CourseModules)
