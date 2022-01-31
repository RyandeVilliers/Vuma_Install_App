from rest_framework import serializers

from core.models import Status

class StatusSerializer(serializers.ModelSerializer):
    """Serializer for status objects"""

    class Meta:
        model = Status
        fields = ('id', 'status', 'notes', 'date', 'user')
        read_only_fields = ('id',)