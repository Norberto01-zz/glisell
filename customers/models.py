from django.db import models
from django.utils.html import format_html
from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel, FieldRowPanel

from wagtail.wagtailcore import hooks
from category.models import Category, CustomerType
from accounting.models import AbsSnippet
from glisell4.settings import STATIC_URL


# Create your models here.


# HOOKS Declarations
@hooks.register('insert_editor_js')
def editor_js():
    return format_html('<script src="' + STATIC_URL + 'js/customers.js" ></script>')


@hooks.register('insert_editor_css')
def editor_css():
    return format_html('<link rel="stylesheet" href="' + STATIC_URL + 'css/admin.css" type="text/css" />')


@register_snippet
class ClientsTypes(AbsSnippet):    
    class Meta:
        verbose_name = 'Tipo De Cliente'
        verbose_name_plural = 'Tipos De Clientes'


class Customer(CustomerType):
    parent_page_types = ['category.CustomerType']
    subpage_types = []
    address = models.CharField(verbose_name=_('Dirección'), max_length=255, null=True, blank=True)

    client_type = models.ForeignKey(
        'ClientsTypes',
        verbose_name=_('Tipo de cliente'),
        null=True,
        blank=True,
        default=1 or None,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            SnippetChooserPanel('client_type'),
        ], heading='Tipo de cliente', classname='type-info'),
        MultiFieldPanel([
            InlinePanel('customer_business_rel', min_num=1, max_num=1)
        ], heading='Información general', classname='general-info'),

        MultiFieldPanel([
            InlinePanel('customer_personal_rel', label='Contactos', min_num=1),
        ], heading='Contactos', classname='contact-info'),

        MultiFieldPanel([
            InlinePanel('customer_carousel_items'),
        ], heading='Media Files', classname='media-info'),

        MultiFieldPanel([
            InlinePanel('customer_location', min_num=1, max_num=1),
            FieldPanel('address', classname='gmap'),
        ], heading="Ubicación", classname='location-info'),
    ]

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Agregar cliente'
