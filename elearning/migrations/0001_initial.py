# Generated by Django 4.2.2 on 2023-07-03 18:32

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=300)),
                ('content', models.JSONField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('allow_premier', models.BooleanField(default=True)),
                ('category', models.ManyToManyField(related_name='course_category', to='elearning.category')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('avatar', models.ImageField(default='static/elearning/avatar-default.svg', upload_to='')),
                ('billing_address', models.CharField(blank=True, max_length=300, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('is_premier', models.BooleanField(default=False)),
                ('premier_expiration', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Student',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('student_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='elearning.student')),
                ('is_teacher', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Teacher',
            },
            bases=('elearning.student',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=datetime.datetime)),
                ('type', models.CharField(choices=[('p', 'Premier'), ('c', 'Course')], max_length=1)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('status', models.CharField(choices=[('0', 'Initial'), ('1', 'Success'), ('2', 'Pending')], default=0, max_length=1)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_course', to='elearning.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_student', to='elearning.student')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_teacher', to='elearning.teacher'),
        ),
    ]