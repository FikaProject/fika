from .base import FikaBaseFolder
from .interfaces import ICourse, ICourseModule, IModuleSegment
from fika import FikaTSF as _
from zope.interface import implementer
import colander
import deform



@implementer(IModuleSegment)
class ModuleSegment(FikaBaseFolder):
    type_name = "ModuleSegment"
    type_title = _(u"Module segment")
    add_permission = "Add %s" % type_name


def includeme(config):
    config.add_content_factory(ModuleSegment)
    config.add_addable_content("ModuleSegment", "CourseModule")
