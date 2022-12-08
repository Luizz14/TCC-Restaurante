from django.urls import URLPattern, path, include
from .views import caixa, cozinha, cardapio, login, cozinhaPedidoPronto, cozinhaPedidoCancelado, retirarItem, esconderPedidoCardapio, addItemPedido, fecharMesa, addProduto, addFuncionario

urlpatterns = [
    path('', login, name='login'),
    path('caixa/', caixa, name='caixa'),
    
    path('caixa/fecharmesa/<int:id>', fecharMesa, name='fecharMesa'),
    path('caixa/retiraritem/<int:id>', retirarItem, name='retirarItem'),
    path('caixa/addProduto/', addProduto, name='addProduto'),
    path('caixa/addFuncionario/', addFuncionario, name='addFuncionario'),

    path('cozinha/', cozinha, name='cozinha'),
    path('cozinha/pedidopronto/<int:id>/', cozinhaPedidoPronto, name='cozinhaPedidoPronto'),
    path('cozinha/pedidocancelado/<int:id>/', cozinhaPedidoCancelado, name='cozinhaPedidoCancelado'),
    
    path('cardapio/', cardapio, name='cardapio'),
    path('cardapio/esconderpedido/<int:id>', esconderPedidoCardapio, name='esconderPedidoCardapio'),
    path('cardapio/addItemPedido/<int:id>', addItemPedido, name='addItemPedido'),
]