from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
# from location_field.models.plain import PlainLocationField
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from django.utils.translation import ugettext_lazy as _
from cities_light.abstract_models import AbstractCity, AbstractCountry, AbstractRegion
from cities_light.receivers import connect_default_signals
from wagtail.wagtailcore import hooks
from django.utils.html import format_html

# HOOKS Declarations
# @hooks.register('insert_editor_js')
# def editor_js():
#     return format_html('<script src="https://maps.googleapis.com/maps/api/js?sensor=true" ></script>')

@register_snippet
class Country(AbstractCountry):
    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
connect_default_signals(Country)


@register_snippet
class Region(AbstractRegion):
    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regiones'
connect_default_signals(Region)


@register_snippet
class City(AbstractCity):
    timezone = models.CharField(max_length=40)
    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
connect_default_signals(City)


# Create your models here.
class Location(models.Model):
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    # city = models.CharField(max_length=255, null=True, blank=True)
    # country = models.CharField(max_length=255, null=True, blank=True)

    city = models.ForeignKey(
        'City',
        verbose_name=_('Ciudad'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    region = models.ForeignKey(
        'Region',
        verbose_name=_('Region'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    country = models.ForeignKey(
        'Country',
        verbose_name=_('Pais'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    ) 

    panels = [
        FieldPanel('zip_code'),
        SnippetChooserPanel('city'),
        SnippetChooserPanel('region'),
        SnippetChooserPanel('country'),  
    ]


class LodgingLocation(Orderable, Location):
    lodging = ParentalKey('lodging.Lodging', related_name='lodging_location')


class CustomerLocation(Orderable, Location):
    lodging = ParentalKey('customers.Customer', related_name='customer_location')