from rest_framework import serializers

from payroll import models


class AllowanceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AllowanceType
        fields = ["url", "code", "description"]


class AllowanceTypeAccumulatorSerializer(serializers.HyperlinkedModelSerializer):
    type_code = serializers.CharField()
    accumulator_code = serializers.CharField()

    class Meta:
        model = models.AllowanceTypeAccumulator
        fields = ["url", "type_code", "accumulator_code"]


class AllowanceSerializer(serializers.HyperlinkedModelSerializer):
    type_code = serializers.CharField()

    class Meta:
        model = models.Allowance
        fields = ["url", "code", "description", "type_code"]
