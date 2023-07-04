from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# class UserInfoAdmin(UserAdmin):
#     list_display = ['username', 'email', 'is_premier','is_teacher','date_joined', 'last_login']
#     fieldsets = [
#         (None, {'fields': ['username', 'password', 'first_name', 'last_name', 'email']}),
#         ('Permissions', {'fields': ['is_superuser', 'is_staff', 'is_active',
#                                                   'groups', 'user_permissions']}),
#         ('Important dates', {'fields': ['last_login', 'date_joined']}),
#         ('Student information', {'fields': ['avatar', 'bio', 'billing_address', 'phone_number', 'is_premier', 'premier_expiration']}),
#         ('Teacher information', {'fields': ['is_teacher', ]}),
#     ]


# Register your models here.
# admin.site.register(Student,UserInfoAdmin)
admin.site.register(MyUser)
admin.site.register(Category)
admin.site.register(Course)

