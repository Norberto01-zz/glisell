from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel

from category.models import Category, ProductsType, CarouselItem
from accounting.models import AbsSnippet, Taxes
from wagtail.wagtailcore.models import Page, CollectionMember, Orderable
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from django.utils.translation import ugettext_lazy as _
from lodging.models import Lodging
from wagtail.wagtailcore import hooks
from django.utils.html import format_html
from glisell4.settings import STATIC_URL

# HOOKS Declarations
@hooks.register('insert_editor_js')
def editor_js():
    return format_html('<script src="' + STATIC_URL + 'js/products.js" ></script>')

@register_snippet
class ProductsCats(AbsSnippet):
    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas' 


@register_snippet
class ProductTax(Taxes):
    class Meta:
        verbose_name = 'Impuesto'
        verbose_name_plural = 'Impuestos' 


class ProductCatRel(models.Model):
    product = ParentalKey('Product', related_name='products_cats_rels', null=True, on_delete=models.SET_NULL)
    products_category = models.ForeignKey(
        'ProductsCats',
        verbose_name=_('Etiqueta'),
        null=True,
        blank=True,
        default=1 or None,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        SnippetChooserPanel('products_category')
    ]


# Lodgings relationships
class ProductCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('products.Product', related_name='product_carousel_items', null=True, on_delete=models.SET_NULL)


class Supplier(models.Model):
    SUPPLIER = [
        ('0', 'Hotel'),
        ('1', 'Restaurante'),
    ]
    RATES = [
        ('0', 'Fijo'),
        ('1', 'Porcentaje'),
    ]

    product_rel = ParentalKey('Product', related_name='supplier_product_rel', null=True, on_delete=models.SET_NULL)
    supplier_lodging_rel = models.ForeignKey(
        'lodging.Lodging',
        verbose_name=_('Proveedor'),
        related_name="supplier_lodging_rel"
    )
    inline_title = models.CharField(verbose_name=_('Etiqueta'), null=True, blank=True, max_length=255)
    supplier_type = models.CharField(verbose_name=_('Tipo De Proveedor'), default='0', max_length=1, null=True, blank=True, 
                                    choices=SUPPLIER)
    margin_rate = models.CharField(verbose_name=_('Tipo De Margen'), default='1', max_length=1, null=True, blank=True, 
                                   choices=RATES)
    cost_price = models.FloatField(verbose_name=_('Precio Costo'), default=0.0, null=True, blank=True)
    profit_margin = models.FloatField(verbose_name=_('Margen De Venta'), default=0.0, null=True, blank=True)
    sale_price = models.FloatField(verbose_name=_('Precio Venta'), default=0.0, null=True, blank=True)
    panels = [
        # FieldPanel('supplier_type', classname="supplier-type-info"),
        FieldPanel('supplier_lodging_rel', classname="supplier-lodging-info"),
        FieldPanel('inline_title', classname="inline-title-info"),
        FieldPanel('cost_price', classname="cost-price-info"),
        FieldPanel('margin_rate', classname="marging-rate-info"),
        FieldPanel('profit_margin', classname="profit-margin-info"),
        FieldPanel('sale_price', classname="sale-price-info")
    ]

    def __str__(self):
        return self.supplier_lodging_rel.title

    # #Overriding
    # def save(self, *args, **kwargs):
    #     if self.margin_rate == 1:
    #         self.sale_price = self.cost_price + ((self.cost_price * self.profit_margin)/100)
    #     super(Supplier, self).save(*args, **kwargs)


# Create your models here.
class Product(ProductsType):
    parent_page_types = ['category.ProductsType']
    subpage_types = []
    STATUS_OPT = (
        ('0', 'Activo'),
        ('1', 'Inactivo'),
    )
    WARRANTY_CHOICES = [(i, i) for i in range(37)]
    PRODUCT_OF_TYPE = [
        ('0', 'Servicio'),
        ('1', 'Consumible'),
        ('2', 'Almacenable'),
    ]
    product_type = models.CharField(verbose_name=_('Tipo de producto'), default='0', max_length=1,
                                    choices=PRODUCT_OF_TYPE)
    sku = models.CharField(verbose_name=_('SKU'), max_length=255, null=True, blank=True)
    reference = models.CharField(verbose_name=_('Referencia Interna'), max_length=255, null=True, blank=True)
    can_be_sold = models.BooleanField(verbose_name=_('Puede ser vendido'), default=True)
    can_be_bought = models.BooleanField(verbose_name=_('Puede ser comprado'), default=True)
    status = models.CharField(verbose_name=_('Estado'), default=0, max_length=1, choices=STATUS_OPT)
    has_variants = models.BooleanField(verbose_name=_('Tiene variantes?'), default=False)
    warranty = models.IntegerField(verbose_name=_('Garantía en meses'), default=0, choices=WARRANTY_CHOICES)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('product_type', classname="product-type-info"),
            FieldPanel('sku', classname="sku-info"),
            FieldPanel('reference', classname="reference-info"),
            FieldPanel('can_be_sold', classname="sold-info"),
            FieldPanel('can_be_bought', classname="bought-info"),
            FieldPanel('has_variants', classname="variants-info"),
            FieldPanel('warranty', classname="warranty-info"),
        ], heading='Información general', classname='general-product-info'),
        MultiFieldPanel([
            InlinePanel('supplier_product_rel', min_num=1),
        ], heading='Proveedores', classname='supplier-product-info'),
        MultiFieldPanel([
            InlinePanel('products_cats_rels'),
        ], heading='Etiquetas', classname='product-category-info'),
        InlinePanel('product_carousel_items', label="Media Files"),
    ]

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Agregar producto'

# Supplier Relationships
# class LodgingProductRel(models.Model):
#     products_key = ParentalKey('Product', related_name='lodging_product_rel', null=True, on_delete=models.SET_NULL)
