from django.db import models

from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.models import Page


@register_snippet
class Feature(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)


@register_snippet
class StyleType(models.Model):
    title = models.CharField(max_length=255)


@register_snippet
class Language(models.Model):
    title = models.CharField(max_length=255)