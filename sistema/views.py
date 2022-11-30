from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic import RedirectView

from .models import produto, itemPedido, mesa, pessoa, pedido, pagamento
from decimal import Decimal

def login(request):
    return render(request, 'login.html')

def caixa(request):
    #itemPedidos = itemPedido.objects.all()

    #Calcular o valor da mesa:
    for itemPedidos in itemPedido.objects.all():
        qtd = itemPedidos.quantidadeItemPedido
        prod = itemPedidos.produto.valorUnitario
        valorItem = itemPedidos.valorItemPedido

        valorItem = qtd * prod
        print(f'Valor Item: {valorItem}')
        #valorItem.save()

        valorMesas = itemPedidos.pedido.valor

        valorMesas = valorMesas + valorItem 
        print(f'Valor da Mesa: {valorMesas}')
        
    context = {
        'pedidos': pedido.objects.all(),
        'itemPedidos': itemPedido.objects.all(),
    }

    return render(request, 'caixa.html', context)

def cardapio(request):
    produtos = produto.objects.all()
    
    pedidoPronto = itemPedido.objects.filter(statusItem = 'p')
    pedidoAndamento = itemPedido.objects.filter(statusItem='a')
    pedidoCancelado = itemPedido.objects.filter(statusItem='c')

    context = {
        'prod': produtos,
        'pedidoP': pedidoPronto,
        'pedidoA': pedidoAndamento,
        'pedidoC': pedidoCancelado,
        'itemPedidos': itemPedido.objects.all(),
    }


    return render(request, 'cardapio.html', context)

def cozinha(request):
    pedidoPronto = itemPedido.objects.filter(statusItem = 'p')
    pedidoAndamento = itemPedido.objects.filter(statusItem='a')
            
    context = {
        'pedidoP': pedidoPronto,
        'pedidoA': pedidoAndamento,
        'itemPedidos': itemPedido.objects.all(),
    }

    return render(request, 'cozinha.html', context)

def cozinhaPedidoCancelado(request, id):
    pedidoC = itemPedido.objects.get(id=id)
    pedidoC.statusItem = 'c'
    pedidoC.save()
    print('alohah cancelado')
    return redirect(cozinha)

def cozinhaPedidoPronto(request, id):
    pedidoP = itemPedido.objects.get(id=id)
    pedidoP.statusItem = 'p'
    pedidoP.save()
    print('alohah pronto')
    return redirect(cozinha)

def retirarItem(request, id):
    itemPedidos = itemPedido.objects.get(id=id)
    itemPedidos.delete()
    return redirect(caixa)

def pedidosMesa (request, id):
    itemPedidosMesa = itemPedido.objects.get(id=id)

    return redirect(caixa)


