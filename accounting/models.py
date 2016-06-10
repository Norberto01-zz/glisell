from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailcore.models import Page, PageManager, Orderable
from wagtail.wagtailsnippets.models import register_snippet
from django.utils.translation import ugettext_lazy as _
from category.models import AccountingType
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from modelcluster.fields import ParentalKey


# Create your models here.

class AbsSnippet(models.Model):
    title = models.CharField(verbose_name=_("Nombre"), max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Taxes(models.Model):
    TAX_OF_FIELD = [
        ('sales', 'Ventas'),
        ('purchases', 'Compras'),
        ('neither', 'Ninguno'),
    ]
    CAL_OF_TAX = [
        # ('group', 'Grupo de impuestos'),
        ('fixed', 'Monto fijo en precio'),
        ('percent', 'Porcentaje en precio'),
    ]
    name = models.CharField(verbose_name=_("Nombre del impuesto"), max_length=255, null=True, blank=True)
    tax_field = models.CharField(verbose_name=_('Ámbito del impuesto'), max_length=255, default='sales',
                                 choices=TAX_OF_FIELD)
    tax_calculation = models.CharField(verbose_name=_('Cálculo de impuesto'), max_length=255, default='percent',
                                       choices=CAL_OF_TAX)
    amount_of = models.FloatField(verbose_name=_('Importe'), default=0.0)
    include_in_price = models.BooleanField(verbose_name=_('Incluir en el precio'), default=True)
    subsequent_taxable = models.BooleanField(verbose_name=_('Base imponible subsecuente'), default=False)
    apply_to_variants = models.BooleanField(verbose_name=_('Aplicar impuesto a variantes'), default=False)

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('tax_field'),
            FieldPanel('tax_calculation'),
            FieldPanel('amount_of'),
            FieldPanel('include_in_price'),
            FieldPanel('subsequent_taxable'),
            FieldPanel('apply_to_variants'),
        ], heading="Información general"),
        # MultiFieldPanel([
        #     InlinePanel('group_tax_rel'),
        # ], heading="Grupo de impuestos"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
#
# # Lodgings relationships
# class AbsTaxes(Orderable, Taxes):
#     page = ParentalKey('accounting.Taxes', related_name='abstaxes_group')
#
#
# class GroupTaxRel(models.Model):
#     taxes = ParentalKey('Taxes', related_name='group_tax_rel')
#     group_tax = models.ForeignKey(
#         'AbsTaxes',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name="+"
#     )
#
#     panels = [
#         SnippetChooserPanel('group_tax')
#     ]