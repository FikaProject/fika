from zope.interface import Attribute
from zope.interface import Interface
from betahaus.pyracont.interfaces import IBaseFolder


class ISiteRoot(IBaseFolder):
    """ Root object for the application. """


class IUsers(IBaseFolder):
    """ Single object present in the root. Contains IUsers. """

    def get_user_by_email(email, validated = True):
        """ Fetch a user object through an email address. If validated is true, only check validated email addresses.
        """

class IUser(IBaseFolder):
    """ User object. Only contains a userid and mapping to other authentication system. """
    title = Attribute("Name of the user")
    email = Attribute("Email address")


class ICourses(IBaseFolder):
    """ Container for ICourse. """

    def module_used_in(uid):
        """ Return all the course objects that uses this modules uid. """


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



class ISecurity(Interface):
    """ Mixin for all content that should handle groups.
        Principal in this terminology is a userid or a group id.
    """
    
    def get_groups(principal):
        """ Return groups for a principal in this context.
            The special group "role:Owner" is never inherited.
        """

    def check_groups(groups):
        """ Check dependencies and group names. """

    def add_groups(principal, groups, event = True):
        """ Add groups for a principal in this context.
            If event is True, an IObjectUpdatedEvent will be sent.
        """

    def del_groups(principal, groups, event = True):
        """ Delete groups for a principal in this context.
            If event is True, an IObjectUpdatedEvent will be sent.
        """

    def set_groups(principal, groups, event = True):
        """ Set groups for a principal in this context. (This clears any previous setting)
            If event is True, an IObjectUpdatedEvent will be sent.
        """

    def get_security():
        """ Return the current security settings.
        """
    
    def set_security(value):
        """ Set current security settings according to value, that is a list of dicts with keys
            userid and groups.
            Warning! This method will also clear any settings for users not present in value!
            This method will send an IObjectUpdatedEvent.
        """

    def list_all_groups():
        """ Returns a set of all groups in this context. """


class IFlashMessages(Interface):
    """ Handle adding and retrieving flash messages. """
    
    