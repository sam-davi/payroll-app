from rest_framework import viewsets

from payroll import models, serializers


class TaxCodeViewSet(viewsets.ModelViewSet):
    queryset = models.TaxCode.objects.all()
    serializer_class = serializers.TaxCodeSerializer
