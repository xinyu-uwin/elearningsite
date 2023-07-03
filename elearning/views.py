from django.contrib.auth import authenticate, login, logout
from django.shortcuts import *
from django.views import View
from django.views.decorators.csrf import csrf_protect

from .models import *


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

@csrf_protect
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('elearning:homepage')
        else:
            # Invalid login credentials, return error message
            return render(request, 'elearning/login.html', {'error': 'Invalid username or password'})

    return render(request,'elearning/login.html')

def signout(request):
    logout(request)
    return redirect('elearning:homepage')