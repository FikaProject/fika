from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from fika.views.base import BaseView
from fika.models.interfaces import ICourseModule
from fika.models.interfaces import ICourseModules
from fika.models.interfaces import IModuleSegment
from fika.models.module_segment import YoutubeSegment, ImageSegment


class CourseModulesView(BaseView):

    @view_config(context = ICourseModules, renderer = "fika:templates/course_modules.pt")
    def course_modules(self):
        self.response['course_modules'] = self.context.values()
        self.response['courses'] = self.root['courses']
        return self.response

    @view_config(context = ICourseModule, renderer = "fika:templates/course_module.pt")
    def course_module(self):
        self.response['module_segments'] = self.context.values()
        self.response['used_in_courses'] = self.root['courses'].module_used_in(self.context.uid)
        return self.response
    
    @view_config(context = ICourseModule, name="sortup", renderer = "fika:templates/course_module.pt")
    @view_config(context = ICourseModule, name="sortdown", renderer = "fika:templates/course_module.pt")
    def module_segment_sort_up(self):
        course_module = self.context
        
        #depending if we move the segment up or down
        diff = 1
        if self.request.view_name==u'sortup':
            diff = -1
        
        #see what position the segment has now
        segment = course_module.get(self.request.GET.get('segment'))
        thisSegmentOrder = int(segment.get_field_value('order',()))
        
        #switch place with all segments that are currently on the position the target segment is going to
        for loopsegment in sorted(course_module.values(), key=lambda segment: int(segment.get_field_value('order', ()))):
            if int(loopsegment.get_field_value('order',()))==thisSegmentOrder+diff:
                loopsegment.set_field_value('order', thisSegmentOrder)
        #move the target segment
        segment.set_field_value('order', thisSegmentOrder+diff)
        
        #fix the number of the ordering
        self.recalculate_segment_order(self.context)
        
        self.response['module_segments'] = self.context.values()
        self.response['used_in_courses'] = self.root['courses'].module_used_in(self.context.uid)
        return HTTPFound(location = self.request.resource_url(self.context))
    
    
    def recalculate_segment_order(self, course_module):
        segments = sorted(course_module.values(), key=lambda segment: int(segment.get_field_value('order', ())))
        
        firstSegmentOrder = int(segments[0].get_field_value('order', ()))
        
        #import pdb; pdb.set_trace()
        
        #set the first segment on place 0, and move all the other segments the same amount
        for segment in segments:
            segment.set_field_value('order', int(segment.get_field_value('order', ())) -firstSegmentOrder)
        
        
        print ""
        prevOriginal = 0
        prev = 0
        #make sure the ordering of segments is without gaps
        for segment in segments:
            current = int(segment.get_field_value('order', ()))
            #import pdb; pdb.set_trace()
            print "current " + str(current) + " prevOriginal " + str(prevOriginal) + " prev " + str(prev)
            if current == prevOriginal:
                current = prev
            else:
                if current > prev + 1:
                    current = prev + 1
            prevOriginal = segment.get_field_value('order', ())
            prev = current
            print "new "+str(current)
            segment.set_field_value('order', current)
    

    @view_config(context = IModuleSegment, renderer = "fika:templates/form.pt")
    def module_segment(self):
        self.response['form'] = self.context.render(self.request, self)
        return self.response