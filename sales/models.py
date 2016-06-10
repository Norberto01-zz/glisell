from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, TabbedInterface, ObjectList
from wagtail.wagtailcore.models import Page
from django.utils.translation import ugettext_lazy as _
from category.models import SalesType, SequenceTypes
from customers.models import Customer
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from accounting.models import AbsSnippet, Taxes
from em_sequence.models import EmSequence
from products.models import Product, ProductTax, Supplier
from lodging.models import Lodging
from contacts.models import FiscalPosition
from wagtail.wagtailcore import hooks
from django.utils.html import format_html
from glisell4.settings import STATIC_URL
from django.contrib import admin
import datetime
import hashlib
import pprint

from sales.forms import SalePageForm


@hooks.register('insert_editor_css')
def editor_css():
    return format_html('<link rel="stylesheet" href="' + STATIC_URL + 'css/sales.css" type="text/css" />')


# HOOKS Declarations
@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        '<script src="' + STATIC_URL + 'js/readonly.js" ></script>'
                                       '<script src="' + STATIC_URL + 'js/sales.js" ></script>'
    )


@register_snippet
class PaymentDeadline(AbsSnippet):
    class Meta:
        verbose_name = 'Plazo de pago'
        verbose_name_plural = 'Plazos de pagos'


# Taxes relationships
class TaxSaleRel(models.Model):
    sales = ParentalKey('Sale', related_name='tax_sale_rel', null=True, on_delete=models.SET_NULL)
    sale_tax = models.ForeignKey(
        'products.ProductTax',
        verbose_name=_('Impuesto'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    panels = [
        SnippetChooserPanel('sale_tax')
    ]


# CLASS SALE LINE RELATIONSHIPS **********
class SaleProductInline(models.Model):
    # Constants, LISTS & CONFIGS --------
    DISCOUNT_RATE = [
        ('fixed', 'Monto Fijo'),
        ('percent', 'Porcentaje'),
    ]
    SUPPLIER = [
        (0, 'Hoteles'),
        (1, 'Restaurantes'),
    ]
    LENGHT = [(i, str(i) + ' Noche') if i == 1 else (i, str(i) + ' Noches') for i in range(1, 16)]

    # PARENTAL KEY RELATIONSHIP -------- 
    sale_inline = ParentalKey('Sale', related_name='sale_inline_rels', null=True, on_delete=models.SET_NULL)

    # sale-head-group FIELDS -------- 
    supplier_type = models.IntegerField(verbose_name=_('Clasificación'), null=True, default='0', choices=SUPPLIER)
    apply_discount = models.BooleanField(verbose_name=_('Tiene descuento?'), default=False)
    discount_type = models.CharField(verbose_name=_('Tipo de descuento'), max_length=1, null=True, blank=True,
                                     choices=DISCOUNT_RATE)
    # sale-passengers-group FIELDS Passengers --------
    num_of_adults = models.IntegerField(verbose_name=_('Adultos'), choices=[(i, i) for i in range(1, 7)], default=1)
    num_of_children = models.IntegerField(verbose_name=_('Niños'), choices=[(i, i) for i in range(0, 4)], default=0)
    child_num_1_age = models.IntegerField(verbose_name=_('Edad'), choices=[(i, i) for i in range(18)], default=0)
    child_num_2_age = models.IntegerField(verbose_name=_('Edad'), choices=[(i, i) for i in range(18)], default=0)
    child_num_3_age = models.IntegerField(verbose_name=_('Edad'), choices=[(i, i) for i in range(18)], default=0)

    # sale-inline-group FIELDS --------
    arrival_date = models.DateField(default=datetime.date.today, null=True, blank=True, verbose_name='Llegada')
    supplier = models.ForeignKey(
        'lodging.Lodging',
        verbose_name=_('Suplidor'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    duration = models.IntegerField(verbose_name=_('Duración'), choices=LENGHT, default=1)
    product_sale_rel = models.ForeignKey(
        'products.Product',
        verbose_name=_('Producto'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    description = models.CharField(verbose_name=_('Descripción'), max_length=255, null=True, blank=True)
    discount = models.PositiveSmallIntegerField(verbose_name=_('Descuento'), null=True, blank=True)
    sale_qty = models.PositiveSmallIntegerField(verbose_name=_('# De Hab.'), choices=[(i, i) for i in range(1, 10)],
                                                default=1)
    sale_price = models.FloatField(verbose_name=_('Precio'), null=True, blank=True)
    sub_total_inline = models.FloatField(verbose_name=_('Sub-total'), null=True, blank=True)
    total_amount_inline = models.FloatField(verbose_name=_('Total'), null=True, blank=True)

    # PANELS ADMIN CONFIG --------
    panels = [
        MultiFieldPanel([
            FieldPanel('supplier_type', classname='supplier-type-rel sale-head-field'),
            FieldPanel('apply_discount', classname='apply-disc-rel sale-disc-field sale-head-field'),
            # FieldPanel('discount_type', classname='type-disc-rel sale-disc-field sale-head-field'),
        ], classname='sale-head-group'),
        MultiFieldPanel([
            FieldPanel('num_of_adults', classname='num-adults-rel sale-passenger-field'),
            FieldPanel('num_of_children', classname='num-child-rel sale-passenger-field'),
            FieldPanel('child_num_1_age', classname='child-1-age child-age sale-passenger-field'),
            FieldPanel('child_num_2_age', classname='child-2-age child-age sale-passenger-field'),
            FieldPanel('child_num_3_age', classname='child-3-age child-age sale-passenger-field'),
        ], classname='sale-passengers-group'),
        MultiFieldPanel([
            FieldPanel('arrival_date', classname='arrival-date-rel sale-inline-field'),
            FieldPanel('supplier', classname='supplier-sale-rel sale-inline-field'),
            FieldPanel('duration', classname='duration-sale-rel sale-inline-field'),
            FieldPanel('product_sale_rel', classname='product-sale-rel sale-inline-field'),
            FieldPanel('sale_qty', classname='qty-sale-info sale-inline-field sale-num-field'),
            # FieldPanel('description', classname='desc-sale-info sale-inline-field'),
            FieldPanel('discount', classname='discount-sale-rel sale-inline-field sale-num-field'),
            FieldPanel('sale_price', classname='sale-price-info sale-inline-field sale-num-field'),
            FieldPanel('sub_total_inline', classname='sub-total-inline sale-inline-field sale-num-field'),
            FieldPanel('total_amount_inline', classname='total-amount-inline sale-inline-field sale-num-field'),
        ], classname='sale-inline-group')
    ]


def get_journ_sell(journal):
    # journals =
    return journal.objects.filter(type_seq='1').values()


# CLASS SALE **********
class Sale(SalesType):
    parent_page_types = ['category.SalesType']
    subpage_types = []

    SALE_STATUS = [
        (1, 'Presupuesto'),
        (2, 'Abierto'),
        (3, 'Pagado'),
        (4, 'Cancelado'),
        (5, 'Crédito'),
    ]

    parent_type = models.OneToOneField(
        SalesType,
        on_delete=models.CASCADE,
        parent_link=True
    )
    customer = models.ForeignKey(
        'customers.Customer',
        verbose_name=_('Cliente'),
        related_name="+"
    )
    # JOINV = get_journ_sell(SequenceTypes)
    # journal = models.ForeignKey(verbose_name=_('Diario'), max_length=255, null=True, blank=True)
    sale_code = models.CharField(verbose_name=_('Código de venta'), max_length=255, null=True, blank=True)
    accounting_date = models.DateField(default=datetime.date.today, verbose_name='Fecha contable')

    sale_order = models.CharField(verbose_name=_('Orden de venta'), max_length=255, null=True, blank=True)
    invoice_ncf = models.CharField(verbose_name=_('Número de comprobante'), max_length=255, null=True, blank=True)

    sale_state = models.IntegerField(verbose_name=_('Estado'), default=1, choices=SALE_STATUS)
    sub_total = models.FloatField(verbose_name=_('Sub Total Venta'), null=True, blank=True)
    sale_taxes = models.FloatField(verbose_name=_('Impuestos'), null=True, blank=True)
    total_amount = models.FloatField(verbose_name=_('Total Venta'), null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('sale_state', classname='sale-state-info'),
        MultiFieldPanel([
            FieldPanel('accounting_date', classname='accounting-date-info sale-gen-field'),
            FieldPanel('customer', classname='customers-sale-info sale-gen-field'),
            FieldPanel('sequence', classname='journal-inv-info sale-gen-field'),
        ], heading='Información general', classname='sale-general-info'),
        MultiFieldPanel([
            FieldPanel('sale_code', classname='sale-code-info'),
            FieldPanel('invoice_ncf', classname='invoice-ncf-info'),
        ], heading='Códigos de facturación', classname='invoice-code-info'),
        MultiFieldPanel([
            InlinePanel('sale_inline_rels', min_num=1, max_num=10),
        ], heading='Lineas de venta', classname='sale-product-info'),
        MultiFieldPanel([
            InlinePanel('tax_sale_rel'),
        ], heading='Impuestos', classname='taxes-sale-info'),
        MultiFieldPanel([
            FieldPanel('sub_total', classname='sub-total-info'),
            FieldPanel('sale_taxes', classname='sale-taxes-field'),
            FieldPanel('total_amount', classname='total-amount-info'),
        ], heading='Totales', classname='amounts-sale-info')
    ]
    base_form_class = SalePageForm

    def save(self, *args, **kwargs):
        if not self.sale_code and self.sale_state == 1:
            parent = self.get_parent()
            sc = SalesType.objects.get(pk=parent.pk)
            code = sc.sequence
            pad = ""
            for i in range(code.padding - len(str(code.number_next))):
                pad += "0"

            seq = '{}{}{}{}'.format(code.prefix, pad, code.number_next, code.suffix)
            self.sale_code = seq

            code.number_actual = code.number_next
            code.number_next += code.number_increment
            code.save()
        self.title = '{} {} {}'.format(self.sale_code, self.customer.title, self.accounting_date)

        super(Sale, self).save(*args, **kwargs)

    def unpublish(self, set_expired=False, commit=True):
        if self.sale_state:
            self.sale_state = 4
        super(Sale, self).unpublish(set_expired, commit)

    def cancel(self):
        self.sale_state = 4
        self.save()

    def serve(self, request, *args, **kwargs):
        pp = pprint.PrettyPrinter(depth=6)
        # pp.pprint(request.GET)
        pp.pprint(request)
        # if request.POST:
        #     is_cancelling = bool(request.POST.get('action-cancel'))
        #     if is_cancelling:
        #         pp.pprint("Is canceling...!!!")
        return render(request, self.template, self.get_context(request))

    class Meta:
        verbose_name = 'V&F'
        verbose_name_plural = 'V&F'
        # def save_revision(self, *args, **kwargs):
        #     return super(Sale, self).save_revision(*args, **kwargs)
        # edit_handler = TabbedInterface([
        #     ObjectList(content_panels, heading='Contenido'),
        #     # ObjectList(sidebar_content_panels, heading='Sidebar content'),
        #     ObjectList(Page.promote_panels, heading='Configuración'),
        #     ObjectList(Page.settings_panels, heading='Publicación', classname="settings"),
        # ])
