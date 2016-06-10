from django.shortcuts import render
from rest_framework import renderers
from rest_framework import routers, serializers, viewsets
from customers.serializers import CustomerSerializer, FiscalSerializer
from contacts.models import FiscalPosition
from django.shortcuts import render, redirect, get_object_or_404
from wagtail.wagtailcore.models import Page
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from customers.models import Customer
import pprint


# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class FiscalViewSet(viewsets.ModelViewSet):
    queryset = FiscalPosition.objects.all()
    serializer_class = FiscalSerializer

