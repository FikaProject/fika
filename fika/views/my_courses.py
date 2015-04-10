from pyramid.httpexceptions import HTTPFound

from arche.views.base import ContentView
from arche import security
from arche import _
from fika.models.interfaces import IFikaUser

class MyCoursesView(ContentView):
    title = _('My Courses')

    def __call__(self):
        
        def _get_first_unfinished_page(courseuid):
            course = self.resolve_uid(courseuid)
            
            noModulesCompleted = True
            for coursemodule in course.values():
                if coursemodule.uid in self.profile.completed_course_modules:
                    noModulesCompleted = False
                    break
            if noModulesCompleted:
                return course
            
            for coursemodule in course.values():
                if coursemodule.uid not in self.profile.completed_course_modules:
                    return coursemodule
            return course
        
        response = {'contents': [x for x in self.context.values() if getattr(x, 'listing_visible', False)]}
        response['course_percentage'] = {}
        response['completed_courses'] = ()
        user = self.root['users'].get(self.request.authenticated_userid, None)
        if user:
            response['fikaProfile'] = IFikaUser(user)
            for uid in response['fikaProfile'].courses:
                course = self.resolve_uid(uid)
                completed_modules = 0
                for course_module in course.values():
                    if(course_module.uid in response['fikaProfile'].completed_course_modules):
                        completed_modules += 1
                if len(course) <= 0:
                    response['course_percentage'][uid] = 0
                else:
                    response['course_percentage'][uid] = round(completed_modules / float(len(course)) * 100.0, 2); 
                if completed_modules == len(course):
                    response['completed_courses'] += (course.uid ,)
        else:
            return HTTPFound(location = self.request.resource_url(self.request.root, 'login'))
        
        response['get_first_unfinished_page'] = _get_first_unfinished_page
        return response
    
    
def includeme(config):
    config.add_view(MyCoursesView,
                    name = 'view',
                    permission = security.PERM_VIEW,
                    renderer = "fika:templates/my_courses.pt",
                    context = 'arche.interfaces.IRoot')
    config.add_content_view('Root', 'view', MyCoursesView)
