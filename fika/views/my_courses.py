from arche.views.base import ContentView
from arche import security
from arche import _
from fika.models.interfaces import IFikaUser

class MyCoursesView(ContentView):
    title = _('My Courses')

    def __call__(self):
        response ={'contents': [x for x in self.context.values() if getattr(x, 'listing_visible', False)]}
        response['course_percentage'] = {}
        response['completed_courses'] = ()
        user = self.root['users'].get(self.request.authenticated_userid, None)
        if user:
            response['profile'] = IFikaUser(user)
            for uid in response['profile'].courses:
                course = self.resolve_uid(uid)
                completed_modules = 0
                for course_module in course.course_modules:
                    if(course_module in response['profile'].completed_course_modules):
                        completed_modules += 1
                response['course_percentage'][uid] = round(completed_modules / float(len(course.course_modules)) * 100.0, 2); 
                if completed_modules == len(course.course_modules):
                    response['completed_courses'] += (course.uid ,)
        #import pdb;pdb.set_trace()
        return response


def includeme(config):
    config.add_view(MyCoursesView,
                    name = 'my_courses_view',
                    permission = security.PERM_VIEW,
                    renderer = "fika:templates/my_courses.pt",
                    context = 'arche.interfaces.IBase')
    config.add_content_view('Root', 'my_courses_view', MyCoursesView)
