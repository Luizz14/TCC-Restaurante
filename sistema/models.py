from django.db import models
from stdimage.models import StdImageField

# Signals
from django.db.models import signals
from django.template.defaultfilters import slugify

class categoria(models.Model):
    nomeCategoria = models.CharField('nome', max_length=50)

class produto(models.Model): 
    nomeProduto = models.CharField('nome', max_length=45)
    descricaoProduto = models.CharField('descricao', max_length=90)
    valorUnitario = models.DecimalField('valor', max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(categoria, on_delete=models.CASCADE)

def produto_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nomeProduto)

signals.pre_save.connect(produto_pre_save, sender=produto)

class pessoa(models.Model):
    nome = models.CharField('nome', max_length= 50)
    cpf = models.CharField('cpf', max_length=11)
    senha = models.CharField('senha', max_length=8)
    telefone = models.BigIntegerField('telefone')
    tipo = models.CharField('tipo', max_length=1)

    def __str__(self):
        return self.nome 

class mesa(models.Model):
    numeroMesa = models.IntegerField('numeroMesa')
    statusMesa = models.CharField('statusMesa', max_length=2)
    
class pedido(models.Model):
    dataPedido = models.TimeField('dataHoraPedido')
    pessoa = models.ForeignKey(pessoa, on_delete=models.CASCADE)
    mesa = models.ForeignKey(mesa, on_delete=models.CASCADE)
    valor = 0

class itemPedido(models.Model):
    valorItemPedido = models.DecimalField('valorItemPedido', max_digits=8, decimal_places=2)
    quantidadeItemPedido = models.IntegerField('quantidadeItemPedido')
    statusItem = models.CharField('statusItemPedido', max_length=5)
    pedido = models.ForeignKey(pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(produto, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(pessoa, on_delete=models.CASCADE)

    def calcularMesa(self):
        return self.quantidadeItemPedido * self.produto.valorUnitario



class pagamento(models.Model):
    formaPagamento = models.CharField('formaPagamento', max_length=1)
    dataPagamento = models.DateField('dataPagamento')
    valorPagamento = models.DecimalField('valorPagamento', max_digits=8, decimal_places=2)
    pedido = models.ForeignKey(pedido, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(pessoa, on_delete=models.CASCADE)
    produto = models.ForeignKey(produto, on_delete=models.CASCADE)
    mesa = models.ForeignKey(mesa, on_delete=models.CASCADE)

class calcularMesa:
    pedido_id = 0
    valorTotal = 0
    valorPorcento = 0
    subTotal = 0
    
