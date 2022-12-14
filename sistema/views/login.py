from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic import RedirectView
from datetime import date, datetime
from django.contrib.auth.models import User

from sistema.views.caixa import caixa
from sistema.views.cardapio import cardapio
from sistema.views.cozinha import cozinha

from ..models import produto, itemPedido, mesa, usuario, pedido, pagamento, categoria
from decimal import Decimal

def pagLogin(request):

    return render(request, 'login.html')

def redirecionarLogin(request):
    usuario = request.user
    if usuario.funcao == 'Admin' or usuario.funcao == 'Caixa':
        return redirect(caixa)
    if usuario.funcao == 'Garçom':
        return redirect(cardapio)
    if usuario.funcao == 'Cozinheiro':
        return redirect(cozinha)
    
    