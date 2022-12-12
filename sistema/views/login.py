from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic import RedirectView
from datetime import datetime
from django.contrib.auth import authenticate, login

from sistema.views.caixa import caixa
from sistema.views.cozinha import cozinha

from ..models import produto, itemPedido, mesa, pessoa, pedido, pagamento, categoria
from decimal import Decimal

def loginT(request):


    return render(request, 'login.html')

def autenticacao(request):
    userPOST = request.POST['usuario']
    senhaPOST = request.POST['senha']

    usuario = authenticate(request, username=userPOST, password=senhaPOST)
    if usuario is not None:
    # A backend authenticated the credentials
        login(request, usuario)

        return redirect(cozinha)
    else:
        # No backend authenticated the credentials
        return redirect(caixa)