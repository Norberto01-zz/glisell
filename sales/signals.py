from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete, m2m_changed
from django.conf import settings
from .models import Sale, SaleProductInline
from wagtail.wagtailcore.models import Page
import pprint
import time
import os.path


# @receiver(pre_delete, sender=Sale)
# @receiver(pre_save, sender=SaleProductInline)
@receiver(pre_save, sender=Sale)
@receiver(pre_save, sender=Page)
def model_pre_change(sender, **kwargs):
    # print('ESTO ES PRE SAVE AND DELETE SIGNAL: {}'.format(kwargs['instance'].__dict__))
    pp = pprint.PrettyPrinter(depth=6)
    inst = kwargs['instance']
    # pp.pprint(inst)
    # if inst.live:
    # if hasattr(inst, 'live'):
    #     print("Live")
    #     pp.pprint(inst.live)
    #     pp.pprint(inst.sale_state)
        # inst.sale_state = 2
    # if hasattr(inst, 'sale_state'):
    #     if inst.sale_state == 4:
    #         pp.pprint("Cancelado!")
    #         pp.pprint(inst.sale_state)

    # if inst.sale_state:
    #     pp.pprint(inst.sale_state)




# @receiver(m2m_changed, sender=Sale)
# def model_m2m_changed(sender, **kwargs):
#     # print('Saved: {}'.format(kwargs['instance'].__dict__))
#     print("M2M Changed")
#     pp = pprint.PrettyPrinter(depth=6)
#     pp.pprint(kwargs['instance'].__dict__)


# post_save.connect(sale_created, sender=Sale)

class ReadOnlyException(Exception):
    pass