"""tutorial URL Configuration

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
from django.contrib import admin
from rest_framework import routers
from quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
#router.register(r'^course_description/get_course_description/([A-Z]{3}[0-9]{3})/$', views.CourseDescriptionViewSet.get_course_description)
router.register(r'^course_description/$', views.CourseDescriptionViewSet)
#router.register(r'course_description/SSW690/$', views.CourseDescriptionViewSet.get_course_description)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^course_description/get_course_desription/(?P<search_id>\w+)/', views.CourseDescriptionViewSet),
    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
