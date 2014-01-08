from zope.interface import Attribute
from zope.interface import Interface


class ISiteRoot(Interface):
    """ Root object for the application. """


class IUsers(Interface):
    """ Single object present in the root. Contains IUsers. """


class IUser(Interface):
    """ User object. Only contains a userid and mapping to other authentication system. """


class ICourses(Interface):
    """ Container for ICourse. """


class ICourse(Interface):
    """ Contains references to course modules. """


class ICourseModules(Interface):
    """ Container for ICourseModule. """


class ICourseModule(Interface):
    """ Container for IModuleSegment. Part of a course, or a stand alone object that can be read up on or organised. """


class IModuleSegment(Interface):
    """ Part of a course object. Could be a text, a video or similar. """
