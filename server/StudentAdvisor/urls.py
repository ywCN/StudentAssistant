"""StudentAdvisor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from StudentAdvisor.SAServer import views

router = routers.DefaultRouter()

router.register(r'course_description', views.CourseDescriptionViewSet)
router.register(r'course_description/get_course_description/(?P<search_id>\w+)/', views.CourseDescriptionViewSet)
router.register(r'course_description/get_course_description/(?P<search_call_number>\w+)/', views.CourseDescriptionViewSet)
router.register(r'available', views.AvailableCourseViewSet)
router.register(r'available/get_available_course/(?P<search_dept_id>\w+)/', views.AvailableCourseViewSet)
router.register(r'times', views.CourseTimeViewSet)
router.register(r'times/get_course_time/(?P<search_id>\w+)/', views.CourseTimeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
