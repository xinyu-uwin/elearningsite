import stripe
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import *
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from elearningsite import settings
from .forms import *
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
            student = Student.objects.get(username=username)
            request.session["avatar"] = str(student.avatar)
            request.session["is_premier"] = student.is_premier
            return redirect('elearning:homepage')

        else:
            errors = form.errors
            return render(request, 'elearning/signup.html', {'form': form, 'errors': errors})
    else:
        form = SignUpForm()

    return render(request,'elearning/signup.html',{'form':form,'error':error})


class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(id=self.kwargs['course_id'])
        if request.user.is_authenticated:
            stripe.api_key = settings.STRIPE_SECRET_KEY

            domain = "https://yourdomain.com"
            if settings.DEBUG:
                domain = "http://127.0.0.1:8000"
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'cad',
                        'unit_amount': int(course.price*100),
                        'product_data': {
                            'name': course.name,
                            'images': ['https://wiki.djcsyn.top/download/attachments/4718593/course-default.png'],

                            'description': 'By: %s %s'%(course.teacher.first_name,course.teacher.last_name),

                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=domain + '/success/',
                cancel_url=domain + '/cancel/',
            )
            return redirect(checkout_session.url)
        else:
            return redirect('elearning:login')

class SuccessView(TemplateView):
    template_name = "elearning/success.html"

class CancelView(TemplateView):
    template_name = "elearning/cancel.html"