from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic import RedirectView

from ..models import produto, itemPedido, mesa, pessoa, pedido, pagamento, categoria

def cozinha(request):
    pedidoPronto = itemPedido.objects.filter(statusItem = 'p')
    pedidoAndamento = itemPedido.objects.filter(statusItem ='a')

    context = {
        'pedidoP': pedidoPronto,
        'pedidoA': pedidoAndamento,
        'itemPedidos': itemPedido.objects.all(),
    }

    return render(request, 'cozinha.html', context)

def cozinhaPedidoCancelado(request, id):
    #Pega o id do item pedido
    pedidoC = itemPedido.objects.get(id=id)
    
    #Altera o status do item para cancelado
    pedidoC.statusItem = 'c'

    #Salva no bd
    pedidoC.save()

    return redirect(cozinha)

def cozinhaPedidoPronto(request, id):
    #Pega o id do item pedido
    pedidoP = itemPedido.objects.get(id=id)
    
    #Altera o status do item para pronto
    pedidoP.statusItem = 'p'
    
    #Salva no bd
    pedidoP.save()

    return redirect(cozinha)