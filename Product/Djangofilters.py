import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    places = django_filters.NumberFilter()
    view = django_filters.CharFilter(lookup_expr='icontains')
    cube = django_filters.NumberFilter()
    kg = django_filters.NumberFilter()
    cube_kg = django_filters.NumberFilter()
    price = django_filters.NumberFilter()
    payment = django_filters.NumberFilter()
    debt = django_filters.NumberFilter()
    where_from = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFromToRangeFilter()
    transport = django_filters.CharFilter(lookup_expr='icontains')
    current_place = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = [
            'title', 'places', 'view', 'cube', 'kg', 'cube_kg', 'price',
            'payment', 'debt', 'where_from', 'date', 'transport',
            'current_place', 'status'
        ]
