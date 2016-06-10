from django.shortcuts import render
from rest_framework import renderers
from rest_framework import routers, serializers, viewsets
from sales.serializers import SaleSerializer
from django.shortcuts import render, redirect, get_object_or_404
from wagtail.wagtailcore.models import Page
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from sales.models import Sale
import pprint


# Create your views here.
class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

# def edit(request):
            # Need to reload the page because the URL may have changed, and we
            # need the up-to-date URL for the "View Live" button.

# SalesViewSet.edit()
#     return render(request, 'wagtailadmin/pages/edit.html', {
#         'page': page,
#         'content_type': content_type,
#         'form': form,
#     })