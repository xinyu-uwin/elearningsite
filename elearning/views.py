from django.shortcuts import *
from .models import *
from django.views import View


# Create your views here.
class HomepageView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'elearning/homepage.html')


def courselist(request):
    courses = Course.objects.all()
    content = {
        'courses':courses
    }
    return render(request, 'elearning/courselist.html', content)


class CourseDetailView(View):
    def get(self,request,*args,**kwargs):
        course = get_object_or_404(Course,pk=self.kwargs['course_id'])
        content = {
            'course':course
        }
        return render(request,'elearning/coursedetail.html',content)
