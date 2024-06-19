from rest_framework import serializers

from payroll import models


class RateSerializer(serializers.HyperlinkedModelSerializer):
    numerator_code = serializers.CharField()
    denominator_code = serializers.CharField()

    class Meta:
        model = models.Rate
        fields = [
            "url",
            "code",
            "description",
            "unit",
            "numerator_code",
            "denominator_code",
            "denominator_cap",
            "factor",
            "days_range",
            "reference_date",
        ]
