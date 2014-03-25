from zope.interface import Attribute
from zope.interface import Interface
from betahaus.pyracont.interfaces import IBaseFolder


class ISecurityAware(Interface):
    pass


class ICatalogable(Interface):
    """ Things that will end up in the site roots catalog.
    """


class IBase(IBaseFolder, ISecurityAware):
    pass


class ISiteRoot(IBase):
    """ Root object for the application. """


class IUsers(IBase):
    """ Single object present in the root. Contains IUsers. """

    def get_user_by_email(email):
        """ Fetch a user object through an email address. If validated is true, only check validated email addresses.
        """


class IUser(IBase, ICatalogable):
    """ User object. Only contains a userid and mapping to other authentication system. """
    title = Attribute("Name of the user")
    email = Attribute("Email address")
    completed_course_modules = Attribute("An OOSet of course module IDs that this user have marked as completed.")


class ICourses(IBase):
    """ Container for ICourse. """

    def module_used_in(uid):
        """ Return all the course objects that uses this modules uid. """


class ICourse(IBase, ICatalogable):
    """ Contains references to course modules. """


class ICourseModules(IBase):
    """ Container for ICourseModule. """


class ICourseModule(IBase, ICatalogable):
    """ Container for IModuleSegment. Part of a course, or a stand alone object that can be read up on or organised. """


class IModuleSegment(IBase, ICatalogable):
    """ Part of a module object. """

        
class IMediaObject(IBase, ICatalogable):
    """ Part of a segment object. Could be a text, a video or similar. """

    def render(request, view):
        """ Render this media object. """

class ITextMediaObject(IMediaObject):
    """ Part of a segment object. Contains text. """
    
class IImageMediaObject(IMediaObject):
    """ Part of a segment object. Contains an image. """
    
class IYoutubeMediaObject(IMediaObject):
    """ Part of a segment object. Contains a youtube link. """
    
class IVimeoMediaObject(IMediaObject):
    """ Part of a segment object. Contains a vimeo link. """
    
class IVideoMediaObject(IMediaObject):
    """ Part of a segment object. Contains a video link. """
  
class IAudioMediaObject(IMediaObject):
    """ Part of a segment object. Contains a audio link. """


class IFile(ISecurityAware, ICatalogable):
    """ An uploaded file. """


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
    
