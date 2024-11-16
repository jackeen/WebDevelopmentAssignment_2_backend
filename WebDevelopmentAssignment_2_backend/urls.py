"""
URL configuration for WebDevelopmentAssignment_2_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

from attendance import views as attendance_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/system/', attendance_views.get_system_info),
    path('api/login/', views.obtain_auth_token),
    path('api/logout/', attendance_views.logout),
    path('api/current_user/', attendance_views.get_user_id),

    path('api/', include('attendance.urls')),
]
