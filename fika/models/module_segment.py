import colander
import deform
from zope.interface import implementer

from .base import FikaBaseFolder
from .interfaces import IModuleSegment
from .interfaces import ICourseModule
from .interfaces import ICourse
from fika import FikaTSF as _


#@content_factory('ModuleSegment')
@implementer(IModuleSegment)
class ModuleSegment(FikaBaseFolder):
    addable_to = ("CourseModule",)
#     schemas = {'add': 'ModuleSegmentSchema',
#                'edit': 'ModuleSegmentSchema',
#                'delete': 'DeleteSchema'}
    type_name = "ModuleSegment"
    type_title = _(u"Module segment")
    add_permission = "Add %s" % type_name
    type_title = _(u"Course module")


def includeme(config):
    config.add_content_factory(ModuleSegment)
