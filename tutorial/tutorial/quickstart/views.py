# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group
from quickstart.models import Course
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer, CourseDescriptionSerializer

from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""

	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""

	queryset = Group.objects.all()
	serializer_class = GroupSerializer

class CourseDescriptionViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows course descriptions to be viewed
	"""
	queryset = Course.objects.all()
	serializer_class = CourseDescriptionSerializer
	
	@list_route(methods=['get'])	
	def get_course_description(self, request):
		queryset = Course.objects.all()
		if 'search_id' in self.request.query_params:
			search_id = self.request.query_params['search_id']
		print search_id
		if search_id:
			queryset = queryset.filter(course_id=search_id)
		serializer_class = CourseDescriptionSerializer
		serializer = CourseDescriptionSerializer(queryset, many=True, context=self.get_serializer_context())
		return Response(serializer.data)

class IndividualCourseDescriptionViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows each course descriptions to be viewed
	"""
	def get(self, request, course_id="SSW690"):
		queryset = Course.objects.filter(course_id=course_id)
		serializer_class = CourseDescriptionSerializer

