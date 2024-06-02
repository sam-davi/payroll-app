from rest_framework import viewsets

from payroll import models, serializers


class AccumulatorViewSet(viewsets.ModelViewSet):
    queryset = models.Accumulator.objects.all()
    serializer_class = serializers.AccumulatorSerializer
