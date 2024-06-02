from rest_framework import serializers

from payroll import models
from .accumulator import AccumulatorSerializer


class AllowanceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AllowanceType
        fields = ["url", "code", "description"]


class AllowanceTypeAccumulatorSerializer(serializers.HyperlinkedModelSerializer):
    type_detail = AllowanceTypeSerializer(source="type", read_only=True)
    accumulator_detail = AccumulatorSerializer(source="accumulator", read_only=True)

    class Meta:
        model = models.AllowanceTypeAccumulator
        fields = ["url", "type", "type_detail", "accumulator", "accumulator_detail"]


class AllowanceSerializer(serializers.HyperlinkedModelSerializer):
    type_detail = AllowanceTypeSerializer(source="type", read_only=True)

    class Meta:
        model = models.Allowance
        fields = ["url", "code", "description", "type", "type_detail"]
