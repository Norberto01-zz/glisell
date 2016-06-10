from tkinter import Button
from django.core.urlresolvers import reverse
from wagtailmodeladmin.options import(
    ModelAdmin, ModelAdminGroup, wagtailmodeladmin_register)
from sales.models import Sale
from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin import widgets as wagtailadmin_widgets
import pprint


# class SaleAdmin(ModelAdmin):
#     model = Sale
#     menu_label = 'Ventas'  # ditch this to use verbose_name_plural from model
#     menu_icon = 'doc-full-inverse'
#     search_fields = ('title',)

#
# class MyModelAdminGroup(ModelAdminGroup):
#     menu_label = 'Explorer'
#     menu_icon = 'folder-open-inverse' # change as required
#     menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
#     list_display = ('sub_total')
#     list_filter = ('sub_total')
#     items = (SaleAdmin,)
#
# wagtailmodeladmin_register(MyModelAdminGroup)

@hooks.register('before_serve_page')
def _hook_sale_cancel(page, request, serve_args, serve_kwargs):
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint(request.META.get('canceled'))
    # pp.pprint("Is canceling invoice...!!!")
    # if request.sale_state:
    #     is_cancelling = bool(request.get('action-cancel'))
    #     if is_cancelling:
    #         pp.pprint("Is canceling invoice inside...!!!")
