from zope.interface import implementer

from fika import FikaTSF as _
from fika.models.base import FikaBaseFolder
from fika.models.interfaces import IAssessment


@implementer(IAssessment)
class Assessment(FikaBaseFolder):
    type_title = _(u"Assessment")
    type_name = u"Assessment"
    add_permission = "Add %s" % type_name
    answer = u""


def includeme(config):
    config.add_content_factory(Assessment)
