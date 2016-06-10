from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page, PageManager, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounting.models import AbsSnippet
from category.models import SequenceTypes

# Create your models here.


@register_snippet
class FiscalPosition(AbsSnippet):
    sequence = models.ForeignKey(
        'category.SequenceTypes',
        verbose_name=_('Secuencia'),
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    panels = [
        FieldPanel('title', classname='fptitle-field'),
        MultiFieldPanel([
            SnippetChooserPanel('sequence')
        ], heading='Secuencia', classname='sequence-rule'),
    ]

    class Meta:
        verbose_name = 'Posición Fiscal'
        verbose_name_plural = 'Posiciónes Fiscales'


@register_snippet
class JobPosition(AbsSnippet):
    class Meta:
        verbose_name = 'Cargo Laboral'
        verbose_name_plural = 'Cargos Laborales'


class ContactField(models.Model):
    phone = models.CharField(verbose_name=_('Teléfono'), blank=True, max_length=255, null=True)
    email = models.CharField(verbose_name=_('EMail'), blank=True, max_length=255, null=True)
    # address = models.CharField(blank=True, max_length=255, null=True, verbose_name=_('Dirección')) 

    panels = [
        FieldPanel('phone'), 
        FieldPanel('email'),  
    ]

    class Meta:
        abstract = True


#Supplier Class 
class BusinessContact(ContactField):
    rnc = models.CharField(verbose_name=_('RNC'), blank=True, max_length=255, null=False)
    mobile = models.CharField(verbose_name=_('Celular'), blank=True, max_length=255, null=True)
    website = models.CharField(verbose_name=_('Sitio Web'), blank=True, null=True, max_length=255)
    notes = RichTextField(verbose_name=_('Notas'), blank=True, null=True)
    fis_position = models.ForeignKey(
        'contacts.FiscalPosition',
        verbose_name=_('Posición Fiscal'),
        null=True,
        blank=True,
        default=1 or None,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel('rnc', classname='nic-field'),
        # SnippetChooserPanel('fiscal_position'),
        MultiFieldPanel([ 
            SnippetChooserPanel('fis_position')
        ], classname='fiscal-position'),
        FieldPanel('phone', classname='phone-field'),
        FieldPanel('mobile', classname='mobile-field'),
        FieldPanel('email', classname='email-field'),
        FieldPanel('website', classname='site-field'),
        # FieldPanel('address'),
        FieldPanel('notes', classname='notes-field'),
    ]


#Supplier Class 
class InternalContact(ContactField):
    # parent_page_types = []
    name = models.CharField(verbose_name=_('Nombre'), blank=True, null=True, max_length=255) 
    job_position = models.ForeignKey(
        'JobPosition',
        verbose_name=_('Cargo Laboral'),
        null=True,
        blank=True,
        default=1 or None,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel('name'), 
        SnippetChooserPanel('job_position'),
        FieldPanel('phone'), 
        FieldPanel('email'),
    ]


# Relationship with Lodgings ----
class LodgingBusinessContact(Orderable, BusinessContact):
    lodging = ParentalKey('lodging.Lodging', related_name='lodging_business')


# Relationship with Lodgings ----
class LodgingInternalContact(Orderable, InternalContact):
    lodging = ParentalKey('lodging.Lodging', related_name='lodging_internal')


# Relationship with customers ----
class CustomerBusinessRel(Orderable, BusinessContact):
    business = ParentalKey('customers.Customer', related_name='customer_business_rel')


# Relationship with customers ----
class CustomerPersonalRel(Orderable, InternalContact):
    personal = ParentalKey('customers.Customer', related_name='customer_personal_rel')


