from zope.interface import Attribute
from zope.interface import Interface
from betahaus.pyracont.interfaces import IBaseFolder


class ISiteRoot(IBaseFolder):
    """ Root object for the application. """


class IUsers(IBaseFolder):
    """ Single object present in the root. Contains IUsers. """


class IUser(IBaseFolder):
    """ User object. Only contains a userid and mapping to other authentication system. """


class ICourses(IBaseFolder):
    """ Container for ICourse. """


class ICourse(IBaseFolder):
    """ Contains references to course modules. """


class ICourseModules(IBaseFolder):
    """ Container for ICourseModule. """


class ICourseModule(IBaseFolder):
    """ Container for IModuleSegment. Part of a course, or a stand alone object that can be read up on or organised. """


class IModuleSegment(IBaseFolder):
    """ Part of a course object. Could be a text, a video or similar. """

    def render(request, view):
        """ Render this module segment. """
