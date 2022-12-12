from decimal import Decimal
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
    valorPedido = models.DecimalField('valorPedido', max_digits=8, decimal_places=2)
    porcentagemPedido = models.DecimalField('porcentagemPedido', max_digits=8, decimal_places=2)
    subTotalPedido = models.DecimalField('subTotalPedido', max_digits=8, decimal_places=2)
    pessoa = models.ForeignKey(pessoa, on_delete=models.CASCADE)
    mesa = models.ForeignKey(mesa, on_delete=models.CASCADE)
      
    def retirarServico(self):
        self.calcularPedido(0)

    def calcularPedido(self, percentualServico):
        # if percentualServico is 0:
        #     self.porcentagemPedido = 0
        # else:
        #     self.porcentagemPedido = self.subTotalPedido / percentualServico

        self.porcentagemPedido = 0 if percentualServico is 0 else self.subTotalPedido / percentualServico
        self.valorPedido = self.subTotalPedido + self.porcentagemPedido

    def adicionarItemPedido(self, percentualServico, valorUnitario):
        self.subTotalPedido += Decimal(valorUnitario)
        self.calcularPedido(percentualServico)
    
    def retirarItemPedido(self, percentualServico, valorUnitario):
        self.subTotalPedido -= Decimal(valorUnitario)
        self.calcularPedido(percentualServico)
        

class itemPedido(models.Model):
    valorItemPedido = models.DecimalField('valorItemPedido', max_digits=8, decimal_places=2)
    quantidadeItemPedido = models.IntegerField('quantidadeItemPedido')
    statusItem = models.CharField('statusItemPedido', max_length=5)
    pedido = models.ForeignKey(pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(produto, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(pessoa, on_delete=models.CASCADE)

    def retirarItemPedido(self, qtdItemRetirar):
        self.quantidadeItemPedido -= qtdItemRetirar
        self.valorItemPedido -= self.produto.valorUnitario
        
class pagamento(models.Model):
    formaPagamento = models.CharField('formaPagamento', max_length=1)
    dataPagamento = models.DateField('dataPagamento')
    valorPagamento = models.DecimalField('valorPagamento', max_digits=8, decimal_places=2)
    pedido = models.ForeignKey(pedido, on_delete=models.CASCADE)
    pessoa = models.ForeignKey(pessoa, on_delete=models.CASCADE)
    produto = models.ForeignKey(produto, on_delete=models.CASCADE)
    mesa = models.ForeignKey(mesa, on_delete=models.CASCADE)
