from django import forms
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.forms import WagtailAdminPageForm
from wagtail.wagtailcore.models import Page
from django.utils.translation import ugettext_lazy as _
import pprint
import time

from category.models import SequenceTypes


# from .models import Sale


class SalePageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super(SalePageForm, self).__init__(*args, **kwargs)
        pp = pprint.PrettyPrinter(depth=6)
        journ = SequenceTypes.objects.filter(type_seq='1')
        self.fields['sequence'] = forms.ModelChoiceField(queryset=journ, label=_('Diario'))
        # pp.pprint(journ)
        # pp.pprint("Hola MUNDOS!!!")

    def save(self, commit=True):
        page = super(SalePageForm, self).save(commit=False)
        pp = pprint.PrettyPrinter(depth=6)
        ts = int(time.time())
        code = page.sequence  # SequenceTypes.objects.get(pk=page.sequence.pk)
        # parent = Page.objects
        # pp.pprint(self.get_parent().sequence)
        # pp.pprint("PArentosss...")
        if not page.invoice_ncf and page.sale_state == 2:
            pad = ""
            for i in range(code.padding - len(str(code.number_next))):
                pad += "0"

            seq = '{}{}{}{}'.format(code.prefix, pad, code.number_next, code.suffix)

            page.invoice_ncf = seq

            code.number_actual = code.number_next
            code.number_next += code.number_increment
            code.save()

        if commit:
            page.save()
        return page


