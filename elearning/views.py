from django.shortcuts import *
from .models import *
from django.views import View

# Create your views here.
def homepage(request):
    return render(request,'elearning/homepage.html')

def courselist(request):
    courses = Course.objects.all()
    content = {
        'courses':courses
    }
    return render(request, 'elearning/courselist.html', content)

def coursedeatil(request,course_id):
    course = get_object_or_404(Course,pk=course_id)
    content = {
        'course':course
    }
    return render(request,'elearning/coursedetail.html',content)
