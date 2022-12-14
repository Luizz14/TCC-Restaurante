from decimal import Decimal
from django.db import models
from stdimage.models import StdImageField
from django.contrib.auth.models import User

# Signals
from django.db.models import signals
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)


class usuario(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    telefone = models.CharField('telefone', max_length=15)
    funcao = models.CharField('Função', max_length=12)
    is_staff = models.BooleanField('Membro da equipe', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'telefone', 'funcao']

    def __str__(self):
        return self.email

    objects = UsuarioManager()


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

# class pessoa(User): 
#     cpf = models.CharField('cpf', max_length=11)
#     telefone = models.BigIntegerField('telefone')
#     tipo = models.CharField('tipo', max_length=1)

class mesa(models.Model):
    numeroMesa = models.IntegerField('numeroMesa')
    statusMesa = models.CharField('statusMesa', max_length=2)
    
class pedido(models.Model):
    dataPedido = models.TimeField('dataHoraPedido')
    valorPedido = models.DecimalField('valorPedido', max_digits=8, decimal_places=2)
    porcentagemPedido = models.DecimalField('porcentagemPedido', max_digits=8, decimal_places=2)
    subTotalPedido = models.DecimalField('subTotalPedido', max_digits=8, decimal_places=2)
    usuario = models.ForeignKey(usuario, on_delete=models.PROTECT)
    mesa = models.ForeignKey(mesa, on_delete=models.CASCADE)
      
    def retirarServico(self):
        self.calcularPedido(0)

    def calcularPedido(self, percentualServico):
        if percentualServico is 0:
            self.porcentagemPedido = 0
        else:
            self.porcentagemPedido = self.subTotalPedido / percentualServico

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
    usuario = models.ForeignKey(usuario, on_delete=models.PROTECT)

    def retirarItemPedido(self, qtdItemRetirar):
        self.quantidadeItemPedido -= qtdItemRetirar
        self.valorItemPedido -= self.produto.valorUnitario
        
class pagamento(models.Model):
    formaPagamento = models.CharField('formaPagamento', max_length=9)
    dataPagamento = models.DateField('dataPagamento')
    valorPagamento = models.DecimalField('valorPagamento', max_digits=8, decimal_places=2)
    valorPagamentoSubTotal = models.DecimalField('valorPagamentoSubTotal', max_digits=8, decimal_places=2)
    valorPagamentoServico = models.DecimalField('valorPagamentoServico', max_digits=8, decimal_places=2)
    pedido = models.ForeignKey(pedido, on_delete=models.CASCADE)
    usuario = models.ForeignKey(usuario, on_delete=models.PROTECT)
    mesa = models.ForeignKey(mesa, on_delete=models.CASCADE)
