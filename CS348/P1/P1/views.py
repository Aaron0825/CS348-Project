from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from .models import *
from .forms import *
from .filters import *
import pandas as pd
from datetime import datetime, timedelta


def is_student(user):
    return user.groups.filter(name='Student').exists()
def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

def loginPage (request):
        if request.method == "POST":
                username = request.POST.get("username")
                password = request.POST.get("password")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                        login(request, user)
                        if is_student(user):
                                return redirect("student")
                        elif is_teacher(user):
                                return redirect("teacher")
                else:
                        messages.info(request, "Invalid Credentials")
        context = {}
        return render(request, "login/login.html", context)

def registerPage(request):
        form = CreateUserForm()
        if request.method == "POST":
                form = CreateUserForm(request.POST)
                if form.is_valid():
                        user = form.save()
                        data = request.POST.get('groups')
                        username = form.cleaned_data.get("username")
                        if data==1:
                                group = Group.objects.get(name="Student")
                                user.groups.add(group)
                        elif data==2: 
                                group = Group.objects.get(name="Teacher")
                                user.groups.add(group)
                        messages.success(request, "Account Created For " + username)
                        first_name = user.first_name
                        last_name = user.last_name
                        if is_student(user):
                               math = Student(user=user,first_name=first_name,last_name=last_name)
                               math.save()
                        elif is_teacher(user):
                               math = Teacher(user=user,first_name=first_name,last_name=last_name)
                               math.save()
                        return redirect("login")
        context = {"form": form}
        return render (request, "register/register.html", context)

def logOut(request):
       logout(request)
       return redirect("login")

@transaction.atomic
def studentPage(request):
        student = Student.objects.get(user=request.user)
        with connection.cursor() as cursor:
                cursor.execute("SELECT calculate_student_gpa(%s);", [str(student.student_id)])
        student.refresh_from_db()
        context = {
        'current_class_standing': student.current_class_standing,
        'gpa': student.gpa,
        }
        return render (request, "student/dashboard.html", context)

def studentest(request):
    student = Student.objects.get(user=request.user)
    qs = TestResult.objects.filter(student=student)
    test_filter = TestResultFilter(request.GET, queryset=qs)
    context = {'test_results': test_filter.qs, "myfilter": test_filter}
    return render(request, 'student/tests.html', context)

def studentWork(request):
    student = Student.objects.get(user=request.user)
    qs = HomeworkResult.objects.filter(student=student)
    homework_filter = HomeworkResultFilter(request.GET, queryset=qs)
    context = {'hw_results': homework_filter.qs, "myfilter": homework_filter}
    return render(request, 'student/homework.html', context)

@transaction.atomic
def teacherPage(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT calculate_all_students_gpa();")
    sts = Student.objects.all().order_by('user__last_name')
    myfilter = StudentFilter(request.GET, queryset=sts)
    students = myfilter.qs
    context = {"students": students, "myfilter": myfilter}
    return render(request, 'teacher/classlist.html', context)

def student_detail(request, pk):
    student = Student.objects.get(student_id=pk)
    test_results     = student.tr.order_by('test__date')
    homework_results = student.hr.order_by('homework__date')
    return render(request, "teacher/student_detail.html", {
        "student":          student,
        "test_results":     test_results,
        "homework_results": homework_results,
    })

@transaction.atomic
def student_test_modify(request, pk):
        t = TestResult.objects.get(pk=pk)
        test_pk = t.student.student_id
        form = TRForm(instance=t)
        if request.method == "POST":
                form = TRForm(request.POST, instance=t)
                if form.is_valid():
                        form.save()
                        return redirect("Student_Detail", pk=test_pk)
        context = {"form":form, "test_pk": test_pk}
        return render (request, "teacher/stm.html", context)

@transaction.atomic
def student_test_delete(request, pk):
        order = TestResult.objects.get(pk=pk)
        test_pk = order.student.student_id
        if request.method == "POST":
                order.delete()
                return redirect("Student_Detail", pk=test_pk)
        context = {"order": order}
        return render (request, "teacher/std.html", context)

@transaction.atomic
def student_hw_modify(request, pk):
        h = HomeworkResult.objects.get(pk=pk)
        test_pk = h.student.student_id
        form = HRForm(instance=h)
        if request.method == "POST":
                form = HRForm(request.POST, instance=h)
                if form.is_valid():
                        form.save()
                        return redirect("Student_Detail", pk=test_pk)
        context = {"form":form, "test_pk": test_pk}
        return render (request, "teacher/hwm.html", context)

@transaction.atomic
def student_hw_delete(request, pk):
        order = HomeworkResult.objects.get(pk=pk)
        test_pk = order.student.student_id
        if request.method == "POST":
                order.delete()
                return redirect("Student_Detail", pk=test_pk)
        context = {"order": order}
        return render (request, "teacher/hwd.html", context)

@transaction.atomic
def teacherTest(request):
        with connection.cursor() as cursor:
                cursor.execute("SELECT calculate_all_test_averages();")
        qs = Test.objects.all().order_by('date')
        test_filter = TestFilter(request.GET, queryset=qs)
        context = {
            'tests': test_filter.qs,
            'myfilter': test_filter,
        }
        return render(request, 'teacher/test.html', context)

def teacher_detail(request, pk):
        test = Test.objects.get(pk=pk)
        tr_filter = TestDetailFilter(request.GET, queryset=test.tr.all())
        details  = tr_filter.qs
        return render(request, "teacher/test_detail.html", {
        "test":      test,
        "tr_filter":    tr_filter,
        "details":   details
        })

@transaction.atomic
def test_result_add(request, pk):
        t = Test.objects.get(pk=pk)
        if request.method == "POST":
                form = TGradeForm(request.POST)
                if form.is_valid():
                        tr = form.save(commit=False)
                        tr.test = t
                        tr.save()
                        return redirect("Teacher_Detail", pk=t.pk)
        else:
                form = TGradeForm()

        return render(request, "teacher/result_add.html", {
        "form":    form,
        "test":    t,
        })

@transaction.atomic
def teacher_test_create(request):
        form = TestForm()
        if request.method == "POST":
                form = TestForm(request.POST)
                if form.is_valid():
                        form.save()
                        return redirect("quiz")
        context = {"form":form}
        return render (request, "teacher/create_test.html", context)

@transaction.atomic
def test_result_modify(request, pk):
        t = TestResult.objects.get(pk=pk)
        test_pk = t.test.pk
        form = TRForm(instance=t)
        if request.method == "POST":
                form = TRForm(request.POST, instance=t)
                if form.is_valid():
                        form.save()
                        return redirect("Teacher_Detail", pk=test_pk)
        context = {"form":form, "test_pk": test_pk}
        return render (request, "teacher/modify.html", context)

@transaction.atomic
def test_drop(request, pk):
        order = TestResult.objects.get(pk=pk)
        test_pk = order.test.pk
        if request.method == "POST":
                order.delete()
                return redirect("Teacher_Detail", pk=test_pk)
        context = {"order": order}
        return render (request, "teacher/delete.html", context)

@transaction.atomic
def teacherWork(request):
        with connection.cursor() as cursor:
                cursor.execute("SELECT calculate_all_homework_averages();")
        qs = Homework.objects.all().order_by('date')
        hw_filter = HomeworkFilter(request.GET, queryset=qs)
        context = {
        'homeworks': hw_filter.qs, 'myfilter': hw_filter
        }
        return render(request, 'teacher/assign.html', context)

def hw_detail(request, pk):
        hw = Homework.objects.get(pk=pk)
        hr_filter = HWDetailFilter(request.GET, queryset=hw.hr.all())
        details  = hr_filter.qs
        context = {"hw": hw, "hr_filter": hr_filter, "details": details}
        return render (request, "teacher/hw_detail.html", context)

@transaction.atomic
def teacher_hw_create(request):
        form = HWForm()
        if request.method == "POST":
                form = HWForm(request.POST)
                if form.is_valid():
                        form.save()
                        return redirect("assignment")
        context = {"form":form}
        return render (request, "teacher/create_hw.html", context)

@transaction.atomic
def hw_result_modify(request, pk):
        h = HomeworkResult.objects.get(pk=pk)
        test_pk = h.homework.pk
        form = HRForm(instance=h)
        if request.method == "POST":
                form = HRForm(request.POST, instance=h)
                if form.is_valid():
                        form.save()
                        return redirect("HW_Detail", pk=test_pk)
        context = {"form":form, "test_pk": test_pk}
        return render (request, "teacher/change.html", context)

@transaction.atomic
def hw_drop(request, pk):
        order = HomeworkResult.objects.get(pk=pk)
        test_pk = order.homework.pk
        if request.method == "POST":
                order.delete()
                return redirect("HW_Detail", pk=test_pk)
        context = {"order": order}
        return render (request, "teacher/cancel.html", context)

@transaction.atomic
def hw_result_add(request, pk):
        t = Homework.objects.get(pk=pk)
        if request.method == "POST":
                form = HGradeForm(request.POST)
                if form.is_valid():
                        tr = form.save(commit=False)
                        tr.homework = t
                        tr.save()
                        return redirect("HW_Detail", pk=t.pk)
        else:
                form = HGradeForm()

        return render(request, "teacher/hw_add.html", {
        "form":    form,
        "hw":    t,
        })

