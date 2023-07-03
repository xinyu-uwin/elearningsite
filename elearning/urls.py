from django.urls import path
from elearning import views

app_name = 'elearning'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    # path('aboutus/', views.aboutus, name='aboutus'),
    path('course/<int:course_id>', views.coursedeatil, name='coursedetail'),
    path('course/', views.courselist, name='courselist'),

]
