from arche.api import DCMetadataMixin
from arche.api import LocalRolesMixin
from zope.interface import implementer

from fika.models.base import FikaBaseFolder
from fika.models.interfaces import ICourseModule
from fika import FikaTSF as _


@implementer(ICourseModule)
class CourseModule(FikaBaseFolder, DCMetadataMixin, LocalRolesMixin):
    type_title = _(u"Course module")
    type_name = u"CourseModule"
    add_permission = "Add %s" % type_name


def includeme(config):
    config.add_content_factory(CourseModule)
    config.add_addable_content("CourseModule", "Course")
    config.add_addable_content("Segment", "CourseModule")
