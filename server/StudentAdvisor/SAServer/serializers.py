from rest_framework import serializers
from StudentAdvisor.SAServer.models import Course


class CourseDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializing all of the course descriptions
    """
    class Meta:
        model = Course
        fields = ('course_id', 'course_name', 'course_description', 'semester', 'day', 'time','campus', 'status', 'call_number')


class AvailableCourseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Course
        fields = ('course_id', 'course_name', 'semester', 'day', 'time', 'campus', 'status', 'call_number')


class CourseTimeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Course
        fields = ('course_id', 'time')
