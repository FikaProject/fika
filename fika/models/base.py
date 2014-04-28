from arche.resources import Content
from zope.interface import implementer

from fika.models.interfaces import IBase


@implementer(IBase)
class FikaBaseFolder(Content):
    pass
