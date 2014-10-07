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
            for uid in course.course_modules:
                if uid in self.profile.completed_course_modules:
                    noModulesCompleted = False
                    break
            if noModulesCompleted:
                return 0
            
            for uid in course.course_modules:
                if uid not in self.profile.completed_course_modules:
                    for (k,v) in course.cm_pages().items():
                        if v == uid:
                            return k
            return 0
        
        response ={'contents': [x for x in self.context.values() if getattr(x, 'listing_visible', False)]}
        response['course_percentage'] = {}
        response['completed_courses'] = ()
        user = self.root['users'].get(self.request.authenticated_userid, None)
        if user:
            response['fikaProfile'] = IFikaUser(user)
            for uid in response['fikaProfile'].courses:
                course = self.resolve_uid(uid)
                completed_modules = 0
                for course_module in course.course_modules:
                    if(course_module in response['fikaProfile'].completed_course_modules):
                        completed_modules += 1
                if len(course.course_modules) <= 0:
                    response['course_percentage'][uid] = 0
                else:
                    response['course_percentage'][uid] = round(completed_modules / float(len(course.course_modules)) * 100.0, 2); 
                if completed_modules == len(course.course_modules):
                    response['completed_courses'] += (course.uid ,)
        
        response['get_first_unfinished_page'] = _get_first_unfinished_page
        return response
    
    
    


def includeme(config):
    config.add_view(MyCoursesView,
                    name = 'view',
                    permission = security.PERM_VIEW,
                    renderer = "fika:templates/my_courses.pt",
                    context = 'arche.interfaces.IRoot')
    config.add_content_view('Root', 'view', MyCoursesView)
