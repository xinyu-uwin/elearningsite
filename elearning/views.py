from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import *
from django.views import View
from .forms import *
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


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

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            student = Student.objects.get(username=username)
            request.session["avatar"] = str(student.avatar)
            request.session["is_premier"]=student.is_premier
            return redirect('elearning:homepage')
        else:
            # Invalid login credentials, return error message
            return render(request, 'elearning/login.html', {'error': 'Invalid username or password'})

    return render(request,'elearning/login.html')

def signout(request):
    logout(request)
    return redirect('elearning:homepage')

def signup(request):
    error = ''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # load the profile instance created by the signal
            user.save()
            #error = 'Success'
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password2"]
            user = authenticate(request,username=username,password=password)
            login(request, user)
            messages.warning(request, 'Your settings have been saved!')
            return redirect('elearning:homepage')

        else:
            errors = form.errors
            return render(request, 'elearning/signup.html', {'form': form, 'errors': errors})
    else:
        form = SignUpForm()

    return render(request,'elearning/signup.html',{'form':form,'error':error})