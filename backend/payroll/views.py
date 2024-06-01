from django.shortcuts import render
from django.db.models import F

from rest_framework import viewsets
from payroll import models, serializers


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer


class TaxCodeViewSet(viewsets.ModelViewSet):
    queryset = models.TaxCode.objects.all()
    serializer_class = serializers.TaxCodeSerializer


class AllowanceTypeViewSet(viewsets.ModelViewSet):
    queryset = models.AllowanceType.objects.all()
    serializer_class = serializers.AllowanceTypeSerializer


class AllowanceViewSet(viewsets.ModelViewSet):
    queryset = models.Allowance.objects.all()
    serializer_class = serializers.AllowanceSerializer


class AccumulatorViewSet(viewsets.ModelViewSet):
    queryset = models.Accumulator.objects.all()
    serializer_class = serializers.AccumulatorSerializer


class AllowanceTypeAccumulatorViewSet(viewsets.ModelViewSet):
    queryset = models.AllowanceTypeAccumulator.objects.all()
    serializer_class = serializers.AllowanceTypeAccumulatorSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer


class PayGroupViewSet(viewsets.ModelViewSet):
    queryset = models.PayGroup.objects.all()
    serializer_class = serializers.PayGroupSerializer


class PayPeriodViewSet(viewsets.ModelViewSet):
    queryset = models.PayPeriod.objects.all()
    serializer_class = serializers.PayPeriodSerializer


# class AccumulatorValueViewSet(viewsets.ModelViewSet):
#     queryset = models.Accumulator.objects.all()
#     serializer_class = serializers.AccumulatorValueSerializer


# class TransactionAccumulatorViewSet(viewsets.ModelViewSet):
#     queryset = models.Transaction.objects.all()
#     serializer_class = serializers.TransactionAccumulatorSerializer


class RateViewSet(viewsets.ModelViewSet):
    queryset = models.Rate.objects.all()
    serializer_class = serializers.RateSerializer
