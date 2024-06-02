from rest_framework import serializers

from payroll import models


class AccumulatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Accumulator
        fields = ["url", "code", "description", "unit"]
