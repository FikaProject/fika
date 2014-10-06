from zope.interface import Attribute
from zope.interface import Interface

from arche.interfaces import IContent


class IFikaUser(Interface):
    """ Adapter to extend functionality of base fika users.
    """


class ICourses(IContent):
    """ Container for ICourse. """

    def module_used_in(uid):
        """ Return all the course objects that uses this modules uid. """


class ICourse(IContent):
    """ Contains references to course modules. """


class ICourseModules(IContent):
    """ Container for ICourseModule. """


class ICourseModule(IContent):
    """ Container for ISegment. Part of a course, or a stand alone object that can be read up on or organised. """


class ISegment(IContent):
    """ Part of a module object. """


class IImageSlideshow(IContent):
    """ A set of images that is shown as a slideshow. """
