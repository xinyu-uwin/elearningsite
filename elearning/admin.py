from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(PremiePlan)
admin.site.register(HomepageRec)
admin.site.register(CourseEnrollment)

