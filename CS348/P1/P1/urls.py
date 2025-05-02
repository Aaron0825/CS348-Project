"""
URL configuration for P1 project.

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
from . import views
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello World")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.loginPage, name="login"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logOut, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("student/dashboard", views.studentPage, name="student"),
    path("student/test", views.studentest, name="test"),
    path("student/assignment", views.studentWork, name="homework"),
    path("teacher/classlist", views.teacherPage, name="teacher"),
    path("teacher/classlist/detail/<str:pk>/", views.student_detail, name="Student_Detail"),
    path("teacher/classlist/detail/<str:pk>/test_update", views.student_test_modify, name="Student_Test_Modify"),
    path("teacher/classlist/detail/<str:pk>/test_delete", views.student_test_delete, name="Student_Test_Drop"),
    path("teacher/classlist/detail/<str:pk>/hw_update", views.student_hw_modify, name="Student_HW_Modify"),
    path("teacher/classlist/detail/<str:pk>/hw_delete", views.student_hw_delete, name="Student_HW_Drop"),
    path("teacher/test", views.teacherTest, name="quiz"),
    path("teacher/test/detail/<str:pk>/", views.teacher_detail, name="Teacher_Detail"),
    path("teacher/test/detail/<str:pk>/add", views.test_result_add, name="Test_Add"),
    path("teacher/test/create", views.teacher_test_create, name="Test_Create"),
    path("teacher/test/detail/<str:pk>/update", views.test_result_modify, name="Test_Modify"),
    path("teacher/test/detail/<str:pk>/delete", views.test_drop, name="Test_Drop"),
    path("teacher/assignment", views.teacherWork, name="assignment"),
    path("teacher/assignment/detail/<str:pk>/", views.hw_detail, name="HW_Detail"),
    path("teacher/assignment/create", views.teacher_hw_create, name="HW_Create"),
    path("teacher/assignment/detail/<str:pk>/update", views.hw_result_modify, name="HW_Modify"),
    path("teacher/assignment/detail/<str:pk>/delete", views.hw_drop, name="HW_Drop"),
    path("teacher/assignment/detail/<str:pk>/add", views.hw_result_add, name="HW_Add"),
]
