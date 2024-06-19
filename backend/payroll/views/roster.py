from rest_framework import viewsets

from payroll import models, serializers


class RosterViewSet(viewsets.ModelViewSet):
    queryset = models.Roster.objects.all()
    serializer_class = serializers.RosterSerializer


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = models.Shift.objects.all()
    serializer_class = serializers.ShiftSerializer


class RosterShiftViewSet(viewsets.ModelViewSet):
    queryset = models.RosterShift.objects.all()
    serializer_class = serializers.RosterShiftSerializer


class RosterEmployeeViewSet(viewsets.ModelViewSet):
    queryset = models.RosterEmployee.objects.all()
    serializer_class = serializers.RosterEmployeeSerializer
