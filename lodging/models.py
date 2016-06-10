from __future__ import unicode_literals

from django.db import models
from django.utils.html import format_html
from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page, CollectionMember, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks
from glisell4 import settings

from category.models import Category, LodgingType, CarouselItem, LodgingCarouselItem
from contacts.models import LodgingBusinessContact, LodgingInternalContact
from accounting.models import AbsSnippet
from location.models import LodgingLocation


# # HOOKS Declarations
# @hooks.register('insert_editor_js')
# def editor_js():
#     return format_html('<script src="https://maps.googleapis.com/maps/api/js?sensor=false" ></script>')


# @hooks.register('insert_editor_css')
# def editor_css():
#     return format_html('<link rel="stylesheet" href="' \
#                        + settings.STATIC_URL \
#                        + 'css/glisell4.css">')


@register_snippet
class Language(AbsSnippet):
    class Meta:
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas' 


@register_snippet
class Feature(AbsSnippet):
    class Meta:
        verbose_name = 'Característica'
        verbose_name_plural = 'Características' 


@register_snippet
class Style(AbsSnippet):
    class Meta:
        verbose_name = 'Estilo'
        verbose_name_plural = 'Estilos' 


class FeatureLodgingRelation(models.Model):
    lodging = ParentalKey('Lodging', related_name='feature_lodging_relation')
    feature = models.ForeignKey(
        'Feature',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        SnippetChooserPanel('feature')
    ]


class StyleLodgingRelation(models.Model):
    lodging = ParentalKey('Lodging', related_name='style_lodging_relation')
    style = models.ForeignKey(
        'Style',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        SnippetChooserPanel('style')
    ]


class LanguageLodgingRelation(models.Model):
    lodging = ParentalKey('Lodging', related_name='language_lodging_relation')
    language = models.ForeignKey(
        'Language',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        SnippetChooserPanel('language')
    ]

 
class Lodging(LodgingType):
    parent_page_types = ['category.LodgingType']
    subpage_types = []
    qty_rooms = models.IntegerField(verbose_name=_("Rooms"), blank=True, null=True)
    address = models.CharField(verbose_name=_('Dirección'), max_length=255, null=True, blank=True)
    latlng = models.CharField(max_length=255, null=True, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel('lodging_business', label='Información general', min_num=0, max_num=1),
        InlinePanel('lodging_internal', label='Contactos', min_num=0, max_num=10),
        InlinePanel('carousel_items', label="Media Files"),
        MultiFieldPanel([
            InlinePanel('feature_lodging_relation', label="Feature"),
            InlinePanel('style_lodging_relation', label="Style"),
            InlinePanel('language_lodging_relation', label="Language"), 
            FieldPanel('qty_rooms'),
        ], heading="Características"),
        MultiFieldPanel([
            # FieldPanel('latlng', classname="gmap--latlng"),
            InlinePanel('lodging_location', min_num=0, max_num=1),
            FieldPanel('address', classname="gmap"),
        ], heading="Ubicación"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Alojamiento'
        verbose_name_plural = 'Agregar alojamiento'
