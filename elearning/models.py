import datetime

from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class MyUser(User):
    avatar = models.ImageField(default='static/elearning/avatar-default.svg')
    bio = models.TextField(blank=True)
    billing_address = models.CharField(max_length=300,null=True,blank=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    is_premier = models.BooleanField(default=False)
    premier_expiration = models.DateField(blank=True,null=True)
    is_teacher = models.BooleanField(default=False)
    #teach_courses =

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Student'


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300,blank=True)
    image = models.ImageField(default='elearning:static/elearning/course-default.png')
    teacher = models.ForeignKey(MyUser, related_name='course_teacher',on_delete=models.CASCADE)
    category = models.ManyToManyField(Category,related_name='course_category')
    content = models.JSONField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    allow_premier = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    TYPE_CHOICE =[
        ('p','Premier'),
        ('c','Course')
    ]
    STATUS_CHOICES = [
        ('0', 'Initial'),
        ('1', 'Success'),
        ('2', 'Pending'),
    ]
    time = models.DateTimeField(default=datetime.datetime)
    student = models.ForeignKey(MyUser, related_name='payment_student',on_delete=models.PROTECT)
    type = models.CharField(max_length=1,choices=TYPE_CHOICE)
    course = models.ForeignKey(Course,related_name='payment_course',on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=5,decimal_places=2)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=0)

    def __str__(self):
        return str(self.id)


