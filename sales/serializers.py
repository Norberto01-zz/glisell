from rest_framework import serializers
from sales.models import Sale, SaleProductInline
from products.serializers import ProductSerializer


class SaleProSerializer(serializers.ModelSerializer):
    product_sale_rel = ProductSerializer()

    class Meta:
        model = SaleProductInline
        fields = ('id', 'supplier_type', 'apply_discount', 'arrival_date', 'product_sale_rel')


class SaleSerializer(serializers.ModelSerializer):
    sale_inline_rels = SaleProSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = ('id', 'sale_code', 'sale_state', 'sub_total', 'sale_taxes', 'sale_inline_rels', 'total_amount')

