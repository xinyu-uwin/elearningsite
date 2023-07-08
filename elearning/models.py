import datetime

from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
User._meta.get_field('first_name').blank = False
User._meta.get_field('first_name').null = False
User._meta.get_field('last_name').blank = False
User._meta.get_field('last_name').null = False


# Create your models here.
class Student(User):
    avatar = models.ImageField(default='/static/elearning/avatar-default.svg')
    bios = models.TextField(blank=True)
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

    # auto set is_premier status
    def save(self, *args, **kwargs):
        if self.premier_expiration:
            if datetime.date.today() <= self.premier_expiration:
                self.is_premier = True
            else:
                self.is_premier = False
        super().save(*args, **kwargs)



class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name




class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300,blank=True)
    image = models.ImageField(default='/static/elearning/course-default.png')
    teacher = models.ForeignKey(Student, related_name='course_teacher',on_delete=models.CASCADE)
    category = models.ManyToManyField(Category,related_name='course_category')
    content = models.JSONField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    allow_premier = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PremiePlan(models.Model):
    name = models.CharField(max_length=10)
    days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    tag = models.CharField(max_length=5,blank=True,null=True)
    daily = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    def __str__(self):
        display = str(self.days)+'days' + str(self.price)
        return display

    def save(self, *args, **kwargs):
        self.daily = self.price/self.days
        super().save(*args, **kwargs)

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
    student = models.ForeignKey(Student, related_name='payment_student',on_delete=models.PROTECT)
    type = models.CharField(max_length=1,choices=TYPE_CHOICE)
    course = models.ForeignKey(Course,related_name='payment_course',on_delete=models.PROTECT,blank=True,null=True)
    plan = models.ForeignKey(PremiePlan,related_name='payment_plan',on_delete=models.PROTECT,blank=True,null=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=0)

    def __str__(self):
        return str(self.id)


