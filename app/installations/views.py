from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Status, Installation

from installations import serializers

class BaseInstallAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(installation__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-status').distinct()

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class StatusViewSet(BaseInstallAttrViewSet):
    """Manage statuses in the database"""

    queryset = Status.objects.all()
    serializer_class = serializers.StatusSerializer


class InstallationViewSet(viewsets.ModelViewSet):
    """Manage Installations in the database"""
    serializer_class = serializers.InstallationSerializer
    queryset = Installation.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the installations for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.InstallationDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Installation"""
        serializer.save(user=self.request.user)
