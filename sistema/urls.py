from django.urls import URLPattern, path

from .views import caixa, cozinha, garcom

urlpatterns = [
    path('caixa/', caixa, name='caixa'),
    path('cozinha/', cozinha, name='cozinha'),
    path('garcom/', garcom, name='garcom')
]