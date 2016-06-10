from rest_framework_filters import backends
from products.models import Product, ProductTax
from products.serializers import ProductSerializer, SaleTaxSerializer, ProductTaxSerializer
from rest_framework import viewsets
from .filters import ProductFilter


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (backends.DjangoFilterBackend,)
    filter_class = ProductFilter
    # filter_backends = [DjangoFilterBackend]
    # filter_fields = ['supplier_product_rel']


class TaxesViewSet(viewsets.ModelViewSet):
    queryset = ProductTax.objects.all()
    serializer_class = ProductTaxSerializer


class SaleTaxesViewSet(viewsets.ModelViewSet):
    queryset = ProductTax.objects.all()
    serializer_class = SaleTaxSerializer
