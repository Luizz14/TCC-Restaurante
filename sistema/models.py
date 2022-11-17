from django.db import models
from stdimage.models import StdImageField

# Signals
from django.db.models import signals
from django.template.defaultfilters import slugify


class produto(models.Model): 
    nomeProduto = models.CharField('nome', max_length=45)
    descicaoProduto = models.CharField('descricao', max_length=90)
    valorUnitario = models.DecimalField('valor', max_digits=8, decimal_places=2)
    categoriaProduto = models.CharField('categoria', max_length=1)
    

def produto_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nomeProduto)

signals.pre_save.connect(produto_pre_save, sender=produto)

