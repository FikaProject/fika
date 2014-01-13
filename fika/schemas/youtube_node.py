from colander import Invalid
from colander import null
import string

class Youtube(object):
    def serialize(self, node, appstruct):
        if appstruct is null:
            return null
        if not isinstance(appstruct, basestring):
            raise Invalid(node, '%r is not a basestring' % appstruct)
        return appstruct

    def deserialize(self, node, cstruct):
        if cstruct is null:
            return null
        if not isinstance(cstruct, basestring):
            raise Invalid(node, '%r is not a string' % cstruct)
        index = string.find(cstruct, 'v=')
        if index > 0:
            cstruct = cstruct[index+2:]
        index = string.find(cstruct, 'youtu.be/')
        if index > 0:
            cstruct = cstruct[index+9:]
        index = string.find(cstruct, '&')
        if index > 0:
            cstruct = cstruct[:index]
        index = string.find(cstruct, '#')
        if index > 0:
            cstruct = cstruct[:index]
        return cstruct

    def cstruct_children(self, node, cstruct):
        return []