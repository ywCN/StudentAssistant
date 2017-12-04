from django.db import models


# Create your models here.
class Course(models.Model):
    course_id = models.CharField(max_length=6, null=True)
    course_name = models.CharField(max_length=50, null=True)
    course_section = models.CharField(max_length=3, null=True)
    course_description = models.CharField(max_length=500, null=True)
    call_number = models.CharField(max_length=10,null=True)
    status = models.CharField(max_length=50, null=True) 
    seats = models.IntegerField(default=0)
    day = models.CharField(max_length=2, null=True)
    time = models.CharField(max_length=50, null=True)
    campus = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    instructor = models.CharField(max_length=50, null=True)
    semester = models.CharField(max_length=50, null=True)
    start_date = models.CharField(max_length=50, null=True)
    end_date = models.CharField(max_length=50, null=True)
    min_credit = models.FloatField(default=0.0)
    max_credit = models.FloatField(default=0.0)
