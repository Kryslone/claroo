# Generated by Django 5.1 on 2024-11-24 19:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claroapp', '0002_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='claroapp.course')),
                ('students', models.ManyToManyField(blank=True, to='claroapp.student')),
            ],
        ),
    ]
