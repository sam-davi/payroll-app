from rest_framework import serializers

from payroll import models
from .accumulator import AccumulatorSerializer


class RateSerializer(serializers.HyperlinkedModelSerializer):
    numerator_detail = AccumulatorSerializer(source="numerator", read_only=True)
    denominator_detail = AccumulatorSerializer(source="denominator", read_only=True)

    class Meta:
        model = models.Rate
        fields = [
            "url",
            "code",
            "description",
            "numerator",
            "numerator_detail",
            "denominator",
            "denominator_detail",
            "factor",
            "days_range",
            "reference_date",
        ]
