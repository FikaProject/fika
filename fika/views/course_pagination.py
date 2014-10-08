from pyramid.renderers import render
from pyramid.traversal import find_interface

from fika.views.fika_base_view import FikaBaseView
from fika.models.interfaces import ICourse

def render_course_pagination(context, request, view):
    
    course = find_interface(context, ICourse)
    
    def _css_class(obj, context):
        cssclass = 'btn'
        if obj.uid in view.fikaProfile.completed_course_modules:
            cssclass += ' btn-success'
        else:
            cssclass += ' btn-default'
        if obj.uid == context.uid:
            cssclass += ' active'
        return cssclass
    
    
    def _is_first(context):
        return context.uid == course.uid
    
    
    def _is_last(context):
        return context.__name__ == course.keys()[-1]
    
    
    def _get_next(context):
        try:
            if context.uid == course.uid:
                return course[course.keys()[0]]
            pos = tuple(course.keys()).index(context.__name__)            
            return course[course.keys()[pos+1]]
        except IndexError, KeyError:
            return
    
    
    def _get_prev(context):
        if context.uid == course.uid:
            return
        pos = tuple(course.keys()).index(context.__name__)
        if pos == 0:
            return course
        else:
            return course[course.keys()[pos-1]]
    
    
    response = {'context': context,
                '_css_class': _css_class,
                '_is_first': _is_first,
                '_is_last': _is_last,
                '_get_next': _get_next,
                '_get_prev': _get_prev,
                'course': find_interface(context, ICourse)
                }
    return render("fika:templates/course_pagination.pt", response, request = request)