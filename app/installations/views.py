from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Status, Installation

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
        return self.queryset.order_by('-status')

    def perform_create(self, serializer):
        """Create a new status"""
        serializer.save()


class InstallationViewSet(viewsets.ModelViewSet):
    """Manage Installations in the database"""
    serializer_class = serializers.InstallationSerializer
    queryset = Installation.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the installations for the authenticated user"""
        status = self.request.query_params.get('status')
        queryset = self.queryset
        if status:
            status_ids = self._params_to_ints(status)
            queryset = queryset.filter(status__id__in=status_ids)
        return queryset.filter(user=self.request.user)
        

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.InstallationDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new Installation"""
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        print(args)
        print(request.body.json())
        return super().partial_update(request, *args, **kwargs)
