from django.urls import URLPattern, path

from .views import caixa, cozinha, cardapio, inserir

urlpatterns = [
    path('caixa/', caixa, name='caixa'),
    path('cozinha/', cozinha, name='cozinha'),
    path('cardapio/', cardapio, name='cardapio'),
    path('inserir/', inserir, name='inserir')
]