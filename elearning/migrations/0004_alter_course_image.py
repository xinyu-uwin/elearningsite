# Generated by Django 4.2.2 on 2023-07-03 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0003_student_bios_alter_course_teacher_delete_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(default='elearning:static/elearning/course-default.png', upload_to=''),
        ),
    ]
