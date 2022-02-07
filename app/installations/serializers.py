from rest_framework import serializers

from core.models import Status, Installation

class StatusSerializer(serializers.ModelSerializer):
    """Serializer for status objects"""

    class Meta:
        model = Status
        fields = ('id', 'status', 'notes', 'date', 'user')
        read_only_fields = ('id', 'user')


class InstallationSerializer(serializers.ModelSerializer):
    """Serialize an installation"""
    
    status = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Installation.objects.all()
    )

    class Meta:
        model = Installation
        fields = ('id', 'customer_name', 'address', 'appointment_date', 'date_created', 
                    'date_modified', 'status')
        read_only_fields = ('id', )

class InstallationDetailSerializer(InstallationSerializer):
    """Serialize installation detail"""
    status = StatusSerializer(read_only=True)