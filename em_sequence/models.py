from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class EmSequence(models.Model):
    TYPE = [
        ('0', 'Compras'),
        ('1', 'Ventas'),
        ('2', 'Miscelaneo'),
    ]
    name = models.CharField(verbose_name=_('Nombre'), max_length=255, null=True, blank=True)
    code = models.CharField(verbose_name=_('Código de sequencia'), max_length=255, null=True, blank=True)
    active = models.BooleanField(verbose_name=_('Activo'), default=True)
    type_seq = models.CharField(verbose_name=_('Tipo'), choices=TYPE, default='1', max_length=1)
    prefix = models.CharField(verbose_name=_('Prefijo'), max_length=255, null=True, blank=True)
    suffix = models.CharField(verbose_name=_('Sufijo'), max_length=255, null=True, blank=True)
    number_actual = models.PositiveIntegerField(verbose_name=_('Número actual'), default=1,
                                                     help_text="Next number that will be used. "
                                                               "This number can be incremented ")
    number_next = models.PositiveIntegerField(verbose_name=_('Siguiente número'), default=1,
                                              help_text="Next number of this sequence")
    number_increment = models.PositiveIntegerField(verbose_name=_('Incremento'), default=1,
                                                   help_text="The next number of the sequence will"
                                                             " be incremented by this number")
    padding = models.PositiveIntegerField(verbose_name=_('Longitud secuencial'), default=1,
                                          help_text="Longitud secuencial, "
                                                    "entre el número de la secuencia y el afijo.")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
