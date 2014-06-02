from .base import FikaBaseFolder
from .interfaces import ICourse, ICourseModule, IModuleSegment
from fika import FikaTSF as _
from zope.interface import implementer
import colander
import deform



@implementer(IModuleSegment)
class ModuleSegment(FikaBaseFolder):
    addable_to = ("CourseModule",)
    type_name = "ModuleSegment"
    type_title = _(u"Module segment")
    add_permission = "Add %s" % type_name


def includeme(config):
    config.add_content_factory(ModuleSegment)
