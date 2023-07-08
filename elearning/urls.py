from django.urls import path
from elearning import views
from .views import *

app_name = 'elearning'



urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    # path('aboutus/', views.aboutus, name='aboutus'),
    path('course/', views.courselist, name='courselist'),
    path('course/<int:course_id>', views.CourseDetailView.as_view(), name='coursedetail'),
    path('login/', views.userlogin, name='login'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('create-checkout-session/<str:type>/<int:item_id>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("premier/", views.premier, name="premier"),


]
