from rest_framework import serializers

from payroll import models


class RosterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Roster
        fields = ["url", "code", "description", "cycle_length"]


class ShiftSerializer(serializers.HyperlinkedModelSerializer):
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    crosses_midnight = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Shift
        fields = [
            "url",
            "code",
            "description",
            "start_time",
            "end_time",
            "crosses_midnight",
            "unpaid_break",
            "hours",
        ]

    def create(self, validated_data):
        start_time = validated_data.pop("start_time")
        end_time = validated_data.pop("end_time")
        start = start_time.hour * 60 + start_time.minute
        end = end_time.hour * 60 + end_time.minute
        if start_time >= end_time:
            end += 24 * 60
        return models.Shift.objects.create(**validated_data, start=start, end=end)

    def update(self, instance, validated_data):
        start_time = validated_data.get("start_time", instance.start_time)
        end_time = validated_data.get("end_time", instance.end_time)
        start = start_time.hour * 60 + start_time.minute
        end = end_time.hour * 60 + end_time.minute
        if start_time >= end_time:
            end += 24 * 60

        instance.code = validated_data.get("code", instance.code)
        instance.description = validated_data.get("description", instance.description)

        instance.start = start
        instance.end = end
        instance.unpaid_break = validated_data.get(
            "unpaid_break", instance.unpaid_break
        )

        instance.save()
        return instance


class RosterShiftSerializer(serializers.HyperlinkedModelSerializer):
    shift_code = serializers.CharField()
    roster_code = serializers.CharField()
    day = serializers.IntegerField()

    class Meta:
        model = models.RosterShift
        fields = [
            "url",
            "shift_code",
            "roster_code",
            "day",
            "start_time",
            "end_time",
            "hours",
        ]


class RosterEmployeeSerializer(serializers.HyperlinkedModelSerializer):
    employee_code = serializers.CharField()
    roster_code = serializers.CharField()

    class Meta:
        model = models.RosterEmployee
        fields = [
            "url",
            "roster_code",
            "employee_code",
            "effective_start",
            "effective_end",
            "offset",
            "get_shifts",
        ]

    def get_shifts(self, obj):
        return obj.get_shifts()
