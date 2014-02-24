from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import ICourses
from fika import FikaTSF as _


@implementer(ICourses)
class Courses(BaseFolder):
    title = display_name = _(u"Courses")

    def module_used_in(self, uid):
        results = set()
        for obj in self.values():
            if uid in obj.get_field_value('course_modules', ()):
                results.add(obj)
        return results
