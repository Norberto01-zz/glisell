from rest_framework import serializers
from customers.models import Customer
from contacts.models import BusinessContact, FiscalPosition


class FiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalPosition
        fields = ('id', 'title', 'sequence')


class ClientBusSerializer(serializers.ModelSerializer):
    # fis_position = FiscalSerializer(many=True, read_only=True)
    class Meta:
        model = BusinessContact
        fields = ('id', 'rnc', 'phone', 'email', 'mobile', 'fis_position')


class CustomerSerializer(serializers.ModelSerializer):
    customer_business_rel = ClientBusSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'title', 'customer_business_rel')
