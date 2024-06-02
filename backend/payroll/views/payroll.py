from rest_framework import viewsets

from payroll import models, serializers


class PayGroupViewSet(viewsets.ModelViewSet):
    queryset = models.PayGroup.objects.all()
    serializer_class = serializers.PayGroupSerializer


class PayPeriodViewSet(viewsets.ModelViewSet):
    queryset = models.PayPeriod.objects.all()
    serializer_class = serializers.PayPeriodSerializer
