from rest_framework import serializers
from payroll.models import Employee, TaxCode


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "url",
            "user",
            "first_name",
            "middle_name",
            "last_name",
            "tax_number",
            "tax_code",
        ]


class TaxCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaxCode
        fields = ["url", "code", "description"]
