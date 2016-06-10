import django_filters
from rest_framework_filters import filters
from rest_framework_filters.filters import RelatedFilter, AllLookupsFilter
from rest_framework_filters.filterset import FilterSet, LOOKUP_SEP
from .models import Product, Supplier
from lodging.models import Lodging


class LodgingFilter(FilterSet):
    pk = AllLookupsFilter('id')
    title = filters.CharFilter(name='title')

    class Meta:
        model = Lodging


class SupplierFilter(FilterSet):
    supplier_type = filters.CharFilter(name='supplier_type')
    lodging = RelatedFilter(LodgingFilter, name='supplier_lodging_rel')

    class Meta:
        model = Supplier


class ProductFilter(FilterSet):
    pk = AllLookupsFilter('id')
    supplier = RelatedFilter(SupplierFilter, name='supplier_product_rel')

    class Meta:
        model = Product