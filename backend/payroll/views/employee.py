from rest_framework import viewsets

from payroll import models, serializers


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer


class EmployeeHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Employee.objects.earnings_history()
    serializer_class = serializers.EmployeeHistorySerializer


class EmployeeCustomFieldViewSet(viewsets.ModelViewSet):
    queryset = models.EmployeeCustomField.objects.all()
    serializer_class = serializers.EmployeeCustomFieldSerializer


class EmployeeCustomFieldValueViewSet(viewsets.ModelViewSet):
    queryset = models.EmployeeCustomFieldValue.objects.all()
    serializer_class = serializers.EmployeeCustomFieldValueSerializer
