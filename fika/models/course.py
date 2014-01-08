from betahaus.pyracont import BaseFolder
from zope.interface import implementer

from .interfaces import ICourse


@implementer(ICourse)
class Course(BaseFolder):
    pass
