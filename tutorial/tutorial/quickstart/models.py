# -*- coding: utf-8 -*-
from __future__ import unicode_literals
 
from django.db import models
# Create your models here.

#class CourseDescriptionManager(models.Manager):
	#pass

class Course(models.Model):
	#objects = CourseDescriptionManager()
	course_id = models.CharField(max_length=6, null=True)
	course_name = models.CharField(max_length=200, null=True)
	course_description = models.CharField(max_length=500, null=True)
	section_title = models.CharField(max_length=150, null=True)
	call_number = models.CharField(max_length=20, null=True)
	status_seats = models.CharField(max_length=50, null=True)
	days_times = models.CharField(max_length=200, null=True)
	instructor = models.CharField(max_length=200, null=True)
	session_dates = models.CharField(max_length=150, null=True)
	credits = models.CharField(max_length=5, null=True)

