from rest_framework import viewsets

from payroll import models, serializers


class AllowanceTypeViewSet(viewsets.ModelViewSet):
    queryset = models.AllowanceType.objects.all()
    serializer_class = serializers.AllowanceTypeSerializer


class AllowanceViewSet(viewsets.ModelViewSet):
    queryset = models.Allowance.objects.all()
    serializer_class = serializers.AllowanceSerializer


class AllowanceTypeAccumulatorViewSet(viewsets.ModelViewSet):
    queryset = models.AllowanceTypeAccumulator.objects.all()
    serializer_class = serializers.AllowanceTypeAccumulatorSerializer
