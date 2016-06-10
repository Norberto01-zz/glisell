from rest_framework import serializers

from lodging.serializers import LodgingSerializer
from products.models import Product, Supplier, ProductTax
from sales.models import TaxSaleRel
from accounting.models import Taxes


class SupplierSerializer(serializers.ModelSerializer):
    supplier_lodging_rel = LodgingSerializer() 

    class Meta:
        model = Supplier
        fields = ('id', 'inline_title', 'supplier_type', 'cost_price', 'margin_rate', 'profit_margin',
                  'sale_price', 'supplier_lodging_rel')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    supplier_product_rel = SupplierSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'can_be_sold', 'can_be_bought', 'supplier_product_rel')

 
class ProductTaxSerializer(serializers.ModelSerializer): 
    class Meta:
        model = ProductTax
        fields = ('id', 'name', 'tax_field', 'tax_calculation', 'amount_of', 
                  'include_in_price', 'subsequent_taxable', 'apply_to_variants')


class SaleTaxSerializer(serializers.HyperlinkedModelSerializer):
    sale_tax = ProductTaxSerializer(many=True, read_only=True)

    class Meta:
        model = TaxSaleRel
        fields = ('id', 'sale_tax')