from django.urls import path
from elearning import views

app_name = 'elearning'
urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    # path('aboutus/', views.aboutus, name='aboutus'),
    path('course/', views.courselist, name='courselist'),
    path('course/<int:course_id>', views.CourseDetailView.as_view(), name='coursedetail'),
    path('login/', views.userlogin, name='login'),
    path('signout/', views.signout, name='signout'),


]
