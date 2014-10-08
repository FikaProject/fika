from zope.interface import implementer
from arche.api import LocalRolesMixin

from .interfaces import ICourses
from .base import FikaBaseFolder
from fika import FikaTSF as _


@implementer(ICourses)
class Courses(FikaBaseFolder, LocalRolesMixin):
    type_title = title = _("Courses")
    type_name = "Courses"


def includeme(config):
    config.add_content_factory(Courses)
