from zope.interface import implementer

from .interfaces import ICourses
from .base import FikaBaseFolder
from fika import FikaTSF as _


@implementer(ICourses)
class Courses(FikaBaseFolder):
    type_title = title = _("Courses")
    type_name = "Courses"

    def module_used_in(self, uid):
        XXX
        results = set()
        for obj in self.values():
            if uid in obj.get_field_value('course_modules', ()):
                results.add(obj)
        return results


def includeme(config):
    config.add_content_factory(Courses)
