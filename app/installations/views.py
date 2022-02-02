from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Status

from installations import serializers


class StatusViewSet(viewsets.GenericViewSet, 
                    mixins.ListModelMixin, 
                    mixins.CreateModelMixin):
    """Manage statuses in the database"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Status.objects.all()
    serializer_class = serializers.StatusSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-status')

    def perform_create(self, serializer):
        """Create a new status"""
        serializer.save(user=self.request.user)
