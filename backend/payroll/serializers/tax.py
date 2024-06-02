from rest_framework import serializers

from payroll import models


class TaxCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TaxCode
        fields = ["url", "code", "description"]
