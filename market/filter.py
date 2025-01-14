import django_filters
from django import forms
from .models import *

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'placeholder': 'Search by name', 'class': 'forms',})
    )
    description = django_filters.CharFilter(
            lookup_expr='icontains',
            widget=forms.TextInput(attrs={'placeholder': 'Search by description'})
        )
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')
    old_price_min = django_filters.NumberFilter(field_name='old_price', lookup_expr='gte', label='Min Old Price')
    old_price_max = django_filters.NumberFilter(field_name='old_price', lookup_expr='lte', label='Max Old Price')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Category')
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(), label='Color')
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(), label='Size')
    rating_min = django_filters.NumberFilter(field_name='rating', lookup_expr='gte', label='Min Rating')
    rating_max = django_filters.NumberFilter(field_name='rating', lookup_expr='lte', label='Max Rating')

    class Meta:
        model = Product
        fields = ['name', 'description', 'price_min', 'price_max', 'old_price_min', 'old_price_max', 'category', 'color', 'size', 'rating_min', 'rating_max']
