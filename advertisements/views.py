from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions, exceptions
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "delete", "partial_update"]:
            return [IsAuthenticated()]
