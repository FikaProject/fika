from zope.interface import implementer
from arche.api import LocalRolesMixin

from .interfaces import ICourses
from .base import FikaBaseFolder
from fika import FikaTSF as _


@implementer(ICourses)
class Courses(FikaBaseFolder, LocalRolesMixin):
    type_title = title = _("Courses")
    type_name = "Courses"

    def module_used_in(self, uid):
        results = set()
        for obj in self.values():
            if uid in obj.course_modules:
                results.add(obj)
        return results


def includeme(config):
    config.add_content_factory(Courses)
