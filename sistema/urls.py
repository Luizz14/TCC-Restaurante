from django.urls import URLPattern, path, include
from .views.login import pagLogin, redirecionarLogin
from .views.caixa import caixa, fecharMesa, retirarItem, addProduto, addCategoria, addFuncionario, alterarMesa, retirarServico, encerrarDia
from .views.cozinha import cozinha, cozinhaPedidoPronto, cozinhaPedidoCancelado
from .views.cardapio import cardapio, esconderPedidoCardapio, addItemPedido

urlpatterns = [
    path('', pagLogin, name='login'),
    path('redirecionarLogin/', redirecionarLogin, name='redirecionarLogin'),

    path('caixa/', caixa, name='caixa'),
    path('caixa/fecharmesa/<int:id>', fecharMesa, name='fecharMesa'),
    path('caixa/retiraritem/<int:id>', retirarItem, name='retirarItem'),
    path('caixa/addProduto/', addProduto, name='addProduto'),
    path('caixa/addCategoria/', addCategoria, name='addCategoria'),
    path('caixa/addFuncionario/', addFuncionario, name='addFuncionario'),
    path('caixa/alterarMesa/', alterarMesa, name='alterarMesa'),
    path('caixa/retirarServico/<int:id>', retirarServico, name='retirarServico'),
    path('caixa/encerrarDia', encerrarDia, name='encerrarDia'),

    path('cozinha/', cozinha, name='cozinha'),
    path('cozinha/pedidopronto/<int:id>/', cozinhaPedidoPronto, name='cozinhaPedidoPronto'),
    path('cozinha/pedidocancelado/<int:id>/', cozinhaPedidoCancelado, name='cozinhaPedidoCancelado'),
    
    path('cardapio/', cardapio, name='cardapio'),
    path('cardapio/esconderpedido/<int:id>', esconderPedidoCardapio, name='esconderPedidoCardapio'),
    path('cardapio/addItemPedido/<int:id>', addItemPedido, name='addItemPedido'),
]