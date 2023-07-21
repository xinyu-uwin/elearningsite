from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from elearning import views
from .views import *
from django.contrib.auth import views as auth_views

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
    path("profile/", views.profile, name="profile"),
    path("mypremier/", views.mypremier, name="mypremier"),
    path("mycourses/", views.mycourses, name="mycourses"),
    path('password_reset/',auth_views.PasswordResetView.as_view(success_url=reverse_lazy('elearning:password_reset_done'), template_name='elearning/password_reset.html',subject_template_name='elearning/password_reset_subject.txt',
             email_template_name='elearning/password_reset_email.html',), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='elearning/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='elearning/password_reset_confirm.html',success_url=reverse_lazy('elearning:password_reset_complete')),name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='elearning/password_reset_complete.html'),name='password_reset_complete'),
    path('course/search/', views.search, name='search'),
    path('teacher-portal/', views.teacher_portal, name='teacher-portal'),
    path('add-course/', views.add_course, name='add-course'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit-course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete-course'),
    path('teacher/viewcourse/<int:course_id>', views.teacher_viewcourse, name='teacher-viewcourse'),

              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
