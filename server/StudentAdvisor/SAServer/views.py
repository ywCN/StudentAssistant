from django.shortcuts import render

from StudentAdvisor.SAServer.models import Course
from rest_framework import viewsets
from StudentAdvisor.SAServer.serializers import CourseDescriptionSerializer, AvailableCourseSerializer,\
    CourseTimeSerializer
from rest_framework.response import Response
from rest_framework.decorators import list_route


# Create your views here.
class CourseDescriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows course descriptions to be viewed
    """
    queryset = Course.objects.all()
    serializer_class = CourseDescriptionSerializer

    @list_route(methods=['get'])
    def get_course_description(self,request):
        queryset = Course.objects.all()
        search_id = None
        search_call_number = None
        if 'search_id' in self.request.query_params:
            search_id = self.request.query_params['search_id']
        if search_id:
            queryset = queryset.filter(course_id__icontains=search_id)
        if 'search_call_number' in self.request.query_params:
            search_call_number = self.request.query_params['search_call_number']
        if search_call_number:
            queryset = queryset.filter(call_number=search_call_number)
        serializer = CourseDescriptionSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class AvailableCourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all()
    queryset = queryset.exclude(status='Closed')
    serializer_class = AvailableCourseSerializer

    @list_route(methods=['get'])
    def get_available_course(self,request):
        queryset = Course.objects.all()
        search_dept_id = None
        if 'search_dept_id' in self.request.query_params:
            search_dept_id = self.request.query_params['search_dept_id']
        if search_dept_id:
            queryset = queryset.filter(course_id__icontains=search_dept_id)
            queryset = queryset.exclude(status='Closed')
            #unique_query_set = []
            #course_ids = set()
            #for course in queryset:
                #if course.course_id not in course_ids:
                    #unique_query_set.append(course)
                    #course_ids.add(course.course_id)
            #queryset = unique_query_set
        serializer = AvailableCourseSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)    


class CourseTimeViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseTimeSerializer

    @list_route(methods=['get'])
    def get_course_time(self,request):
        queryset = Course.objects.all()
        search_id = None
        if 'search_id' in self.request.query_params:
            search_id = self.request.query_params['search_id']
        if search_id:
            queryset = queryset.filter(course_id=search_id)
        serializer = CourseTimeSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)
