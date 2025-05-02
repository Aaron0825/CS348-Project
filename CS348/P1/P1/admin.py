from django.contrib import admin
from .models import *

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(Homework)
admin.site.register(HomeworkResult)