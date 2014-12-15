from zope.interface import implementer

from fika import FikaTSF as _
from fika.models.base import FikaBaseFolder
from fika.models.interfaces import IAssessment
from fika.models.interfaces import IAssessmentResponse


@implementer(IAssessment)
class Assessment(FikaBaseFolder):
    type_title = _(u"Assessment")
    type_name = u"Assessment"
    add_permission = "Add %s" % type_name
    question = ""
    email = ""

@implementer(IAssessmentResponse)
class AssessmentResponse(FikaBaseFolder):
    type_title = _(u"Assessment Response")
    type_name = u"AssessmentResponse"
    add_permission = "Add %s" % type_name
    user_uid = u""
    answer = u""


def includeme(config):
    config.add_content_factory(Assessment)
    config.add_content_factory(AssessmentResponse)
    config.add_addable_content("AssessmentResponse", "Assessment")
