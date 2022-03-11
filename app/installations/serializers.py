from rest_framework import serializers

from core.models import Status, Installation


class StatusSerializer(serializers.ModelSerializer):
    """Serializer for status objects"""

    class Meta:
        model = Status
        fields = ("id", "status", "notes", "date")
        read_only_fields = ("id",)


class InstallationSerializer(serializers.ModelSerializer):
    """Serialize an installation"""

    class Meta:
        model = Installation
        fields = (
            "id",
            "customer_name",
            "address",
            "appointment_date",
            "date_created",
            "date_modified",
        )
        read_only_fields = ("id",)

    def update(self, instance, validated_data):
        data = self._kwargs["data"]
        status = data.get("status")
        notes = data.get("notes")
        Status.objects.create(installation=instance, status=status, notes=notes)
        return instance


class InstallationDetailSerializer(serializers.ModelSerializer):
    """Serialize installation detail"""

    status = StatusSerializer(many=True)

    class Meta:
        model = Installation
        fields = (
            "id",
            "customer_name",
            "address",
            "appointment_date",
            "date_created",
            "date_modified",
            "status",
        )
        read_only_fields = ("id",)
