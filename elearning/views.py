from datetime import timedelta

import stripe
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import *
from django.utils import timezone
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
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payment_type = self.kwargs['type']
        item_id = self.kwargs['item_id']
        images = []
        description = ''
        print(item_id)
        if payment_type == 'c':
            item = Course.objects.get(id=item_id)
            description = 'By: %s %s'%(item.teacher.first_name,item.teacher.last_name)
            images = ['https://wiki.djcsyn.top/download/attachments/4718593/course-default.png']
        elif payment_type == 'p':
            item = PremiePlan.objects.get(pk=item_id)
            description = '%s days Premier plan' % item.days
            print(item)
        else:
            # Handle invalid type
            pass

        if request.user.is_authenticated:
            domain = "https://yourdomain.com"
            if settings.DEBUG:
                domain = "http://127.0.0.1:8000"

            success_url = f"{domain}/success?session_id={{CHECKOUT_SESSION_ID}}&type={payment_type}&id={item.id}"
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'cad',
                        'unit_amount': int(item.price*100),
                        'product_data': {
                            'name': item.name,
                            'images': images,
                            'description': description,

                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=domain + '/cancel/',
            )
            checkout_session.success_url.replace("{CHECKOUT_SESSION_ID}", checkout_session.id)
            #print(checkout_session.id)
            return redirect(checkout_session.url)
        else:
            return redirect('elearning:login')

class SuccessView(TemplateView):
    template_name = "elearning/success.html"

    def get(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session_id = request.GET.get('session_id')
        session = stripe.checkout.Session.retrieve(session_id)

        payment_type = request.GET.get('type')
        item_id = request.GET.get('id')


        if session.payment_status == 'paid':
            student = Student.objects.get(id=request.user.id)
            if payment_type == 'c':
                course = Course.objects.get(id=item_id)
                Payment.objects.create(
                    time=timezone.now(),
                    student=student,
                    type=payment_type,  # use the type from the URL
                    course=course,
                    status='1',
                )

            elif payment_type == 'p':
                plan = PremiePlan.objects.get(id=item_id)
                Payment.objects.create(
                    time=timezone.now(),
                    student=student,
                    type=payment_type,  # use the type from the URL
                    plan=plan,
                    status='1',
                )
                student.premier_expiration = datetime.date.today() + timedelta(days=plan.days)
                # Save the changes
                student.save()
                request.session["is_premier"] = True
            else:
                pass


        return render(request, self.template_name)

class CancelView(TemplateView):
    template_name = "elearning/cancel.html"

def premier(request):
    plans = PremiePlan.objects.all()
    return render(request,'elearning/premierplan.html',{"plans":plans})