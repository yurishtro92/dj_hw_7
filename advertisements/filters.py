from django_filters import rest_framework as filters
from advertisements.models import Advertisement

class AdvertisementFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    creator = filters.Filter()
    status = filters.Filter()
    class Meta:
        model = Advertisement
        fields = ['created_at', 'creator', 'status']

