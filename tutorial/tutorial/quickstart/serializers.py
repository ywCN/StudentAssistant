from django.contrib.auth.models import User, Group
from rest_framework import serializers
from quickstart.models import Course

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')


class CourseDescriptionSerializer(serializers.HyperlinkedModelSerializer):
	"""
	Serializing all the course descriptions
	"""
	
	class Meta:
		model = Course
		fields = ('course_id', 'course_name', 'course_description')

class GetClassTimeSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Course
		fields = ('course_id', 'course_time')

