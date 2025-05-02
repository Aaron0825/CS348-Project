import django_filters
from .models import *
from django_filters import DateFilter, ChoiceFilter, NumberFilter
from django.db.models import F, Q
import pandas as pd

class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "current_class_standing"]

class TestDetailFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(
        field_name='student__first_name',
        lookup_expr='icontains',
        label='First name'
    )
    last_name = django_filters.CharFilter(
        field_name='student__last_name',
        lookup_expr='icontains',
        label='Last name'
    )

    class Meta:
        model = TestResult
        fields = ['first_name', 'last_name']

class HWDetailFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(
        field_name='student__first_name',
        lookup_expr='icontains',
        label='First name'
    )
    last_name = django_filters.CharFilter(
        field_name='student__last_name',
        lookup_expr='icontains',
        label='Last name'
    )

    class Meta:
        model = HomeworkResult
        fields = ['first_name', 'last_name']

class HomeworkResultFilter(django_filters.FilterSet):
    above_average = django_filters.BooleanFilter(
        label='Only show results above the average',
        method='filter_above_average'
    )

    start_date = DateFilter(
        field_name='homework__date',
        lookup_expr='gte',
        label='Due Date From'
    )
    end_date = DateFilter(
        field_name='homework__date',
        lookup_expr='lte',
        label='Due Date To'
    )

    class Meta:
        model = HomeworkResult
        fields = ["score"]

    def filter_above_average(self, queryset, name, value):
        if value:
            return queryset.filter(score__gt=F('homework__average_score'))
        return queryset


class TestResultFilter(django_filters.FilterSet):
    above_average = django_filters.BooleanFilter(
        label='Only show results above the average',
        method='filter_above_average'
    )

    start_date = DateFilter(
        field_name='test__date',
        lookup_expr='gte',
        label='Test Date From'
    )
    end_date = DateFilter(
        field_name='test__date',
        lookup_expr='lte',
        label='Test Date To'
    )

    class Meta:
        model = TestResult
        fields = ["score"]

    def filter_above_average(self, queryset, name, value):
        if value:
            return queryset.filter(score__gt=F('test__average_score'))
        return queryset


class TestFilter(django_filters.FilterSet):
    start_date = DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Test Date From'
    )
    end_date = DateFilter(
        field_name='date',
        lookup_expr='lte',
        label='Test Date To'
    )

    class Meta:
        model = Test
        fields = ["name", "weight"]

class HomeworkFilter(django_filters.FilterSet):
    start_date = DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Due Date From'
    )
    end_date = DateFilter(
        field_name='date',
        lookup_expr='lte',
        label='Due Date To'
    )

    class Meta:
        model = Homework
        fields = ["name", "weight"]