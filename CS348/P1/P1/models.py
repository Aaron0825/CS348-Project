from django.db import models
from django import forms
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractUser
import pandas as pd
import numpy as np


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    current_class_standing = models.CharField(max_length=2, null=True, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.student_id})"
    
    class Meta:
        indexes = [
            models.Index(fields=['user'], name='student_user_idx'),
            models.Index(fields=['last_name', 'first_name'], name='student_name_idx'),
        ]

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    teacher_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Prof. {self.user.last_name} ({self.teacher_id})"


class Test(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['date'], name='test_date_idx'),
        ]


class TestResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='tr')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='tr')
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.test.name} - {self.score}"

    class Meta:
        indexes = [
            models.Index(fields=['student'], name='tr_student_idx'),
            models.Index(fields=['test'],    name='tr_test_idx'),
            models.Index(fields=['student', 'test'], name='tr_student_test_idx'),
        ]

class Homework(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['date'], name='hw_date_idx'),
        ]


class HomeworkResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='hr')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='hr')
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.student} - {self.homework.name} - {self.score}"
    
    class Meta:
        indexes = [
            models.Index(fields=['student'], name='hr_student_idx'),
            models.Index(fields=['homework'], name='hr_hw_idx'),
            models.Index(fields=['student', 'homework'], name='hr_student_hw_idx'),
        ]
