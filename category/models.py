import datetime

from django.utils.html import format_html
from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page, CollectionMember, Orderable, PageManager
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel, \
    TabbedInterface, ObjectList
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from django.utils.translation import ugettext_lazy as _
from django.db import models
from em_sequence.models import EmSequence


# class EventPageManager(PageManager):
#     """ Custom manager for Event pages """


# class EventPage(Page):
#     start_date = models.DateField(default=datetime.date.today, null=True)

#     objects = EventPageManager()

#     content_panels = Page.content_panels + [
#         FieldPanel('start_date', classname="basic-fields date"), 
#     ]


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class CarouselItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


# Lodgings relationships
class LodgingCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('lodging.Lodging', related_name='carousel_items')


# Customers Relationships
class CustomerCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('customers.Customer', related_name='customer_carousel_items')


class Category(models.Model):
    # subpage_types = ['category.CustomerType', 'category.LodgingType', 'category.ProductsType']
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    created_date = models.DateField(default=datetime.date.today, null=True, blank=True,
                                    verbose_name='Fecha de creación')
    details_field = RichTextField(blank=True, null=True)

    panels = [
        FieldPanel('created_date'),
        FieldPanel('details_field'),
    ]

    class Meta:
        abstract = True


class RootTree(Category, Page):
    subpage_types = ['category.CustomerType', 'category.LodgingType', 'category.ProductsType', 'category.SalesType']

    content_panels = Page.content_panels + [
        FieldPanel('created_date', classname="basic-fields date"),
        FieldPanel('details_field', classname="basic-fields details"),
    ]

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'


class LodgingType(Category, Page):
    parent_page_types = ['category.RootTree']
    subpage_types = ['lodging.Lodging', 'category.LodgingType']
    content_panels = Page.content_panels + [
        FieldPanel('created_date', classname="basic-fields date"),
        FieldPanel('details_field', classname="basic-fields details"),
    ]

    class Meta:
        verbose_name = 'Categoría de alojamiento'
        verbose_name_plural = 'Agregar Categoría de alojamiento'


class CustomerType(Category, Page):
    parent_page_types = ['category.RootTree']
    subpage_types = ['customers.Customer', 'category.CustomerType']
    content_panels = Page.content_panels + [
        FieldPanel('created_date', classname="basic-fields date"),
        FieldPanel('details_field', classname="basic-fields details"),
    ]

    class Meta:
        verbose_name = 'Categoría de clientes'
        verbose_name_plural = 'Agregar Categoría de clientes'


#
# class BlogPage(Page):
#     # field definitions omitted
#
#     content_panels = [
#         FieldPanel('title', classname="full title"),
#         FieldPanel('date'),
#         FieldPanel('body', classname="full"),
#     ]
#     sidebar_content_panels = [
#         SnippetChooserPanel('advert'),
#         InlinePanel('related_links', label="Related links"),
#     ]


class ProductsType(Category, Page):
    parent_page_types = ['category.RootTree']
    subpage_types = ['products.Product', 'category.ProductsType']

    content_panels = Page.content_panels + [
        FieldPanel('created_date', classname="basic-fields date"),
        FieldPanel('details_field', classname="basic-fields details"),
    ]

    class Meta:
        verbose_name = 'Categoría de productos'
        verbose_name_plural = 'Agregar Categoría de productos'


class AccountingType(Category, Page):
    parent_page_types = []
    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel('created_date', classname="basic-fields date"),
        FieldPanel('details_field', classname="basic-fields details"),
    ]

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'


@register_snippet
class SequenceTypes(EmSequence):
    objects = models.Manager()

    class Meta:
        verbose_name = 'Secuencia'
        verbose_name_plural = 'Secuencias'


class SalesType(Category, Page):
    parent_page_types = ['category.RootTree']
    subpage_types = ['sales.Sale']
    sequence = models.ForeignKey(
        'SequenceTypes',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Secuencia'
    )
    content_panels = Page.content_panels + [
        FieldPanel('created_date', classname="basic-fields date"),
        FieldPanel('sequence', classname="basic-fields sequence"),
        FieldPanel('details_field', classname="basic-fields details"),
    ]

    class Meta:
        verbose_name = 'F&V'
        verbose_name_plural = 'F&V'
