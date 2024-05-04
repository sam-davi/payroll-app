from django.shortcuts import render

from rest_framework import viewsets
from payroll.models import Employee, TaxCode
from payroll.serializers import EmployeeSerializer, TaxCodeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class TaxCodeViewSet(viewsets.ModelViewSet):
    queryset = TaxCode.objects.all()
    serializer_class = TaxCodeSerializer
