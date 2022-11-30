from django.urls import URLPattern, path, include
from .views import caixa, cozinha, cardapio, login, cozinhaPedidoPronto, cozinhaPedidoCancelado, retirarItem, pedidosMesa

urlpatterns = [
    path('login/', login, name='login'),
    path('caixa/', caixa, name='caixa'),
    path('caixa/<int:id>', retirarItem, name='retirarItem'),
    path('caixa/<int:id>', pedidosMesa, name='pedidoMesa'),
    path('cozinha/', cozinha, name='cozinha'),
    path('cozinha/<int:id>/', cozinhaPedidoCancelado, name='cozinhaPedidoCancelado'),
    path('cozinha/<int:id>/', cozinhaPedidoPronto, name='cozinhaPedidoPronto'),
    path('cardapio/', cardapio, name='cardapio'),
]