from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic import RedirectView
from time import time

from .models import produto, itemPedido, mesa, pessoa, pedido, pagamento
from decimal import Decimal

def login(request):
    return render(request, 'login.html')

def caixa(request):
    #if itemPedidos == itemPedidos.
    
    #Calcular o valor da mesa:
    for itemPedidos in itemPedido.objects.all():
        qtd = itemPedidos.quantidadeItemPedido
        prod = itemPedidos.produto.valorUnitario
        valorItem = itemPedidos.valorItemPedido

        #Calcula o valor total dos item pedidos
        valorItem = qtd * prod
        #print(f'Valor Item: {valorItem}')
        #valorItem.save()

        #Armazena valor da tabela
        valorMesas = itemPedidos.pedido.valor

        #Calcula o valor total da mesa
        valorMesas = valorMesas + valorItem 
        #print(f'Valor da Mesa: {valorMesas}')

    context = {
        'pedidos': pedido.objects.all(),
        'itemPedidos': itemPedido.objects.all(),
    }

    return render(request, 'caixa.html', context)

def fecharMesa(request, id):
    #Fechamento da mesa
    pedidoId =  pedido.objects.get(id=id)
    
    for itemPedidos in itemPedido.objects.all():
        if itemPedidos.quantidadeItemPedido <= 0:
            pedidoId =  pedido.objects.get(id=id)
            mesaId = pedidoId.mesa
            mesaId.statusMesa = 'f'
            mesaId.save()
   
    
    mesaId = pedidoId.mesa
    mesaId.statusMesa = 'f'

    mesaId.save()

    return redirect(caixa)


def retirarItem(request, id):
    itemPedidos = itemPedido.objects.get(id=id)

    if itemPedidos.quantidadeItemPedido > 1:
        #Diminuir a quantidade do item
        qtdItem = itemPedidos.quantidadeItemPedido
        qtdItem = qtdItem - 1

        #Diminuir o valor do item
        valorItem = itemPedidos.valorItemPedido
        valorItem = valorItem - itemPedidos.produto.valorUnitario

        itemPedidos.quantidadeItemPedido = qtdItem
        itemPedidos.valorItemPedido = valorItem

        itemPedidos.save()
    else:  
        itemPedidos.delete()
        
    #Excluir mesa caso não tenha mais nenhum pedido
    for item in itemPedido.objects.all():
        mesas = 0 
        if item.pedido_id == itemPedidos.pedido_id:
            mesas = mesas + 1
    if mesas == 1:
        print(f'oia {mesas}')
    else:
        print(f'taporar {mesas}')
            
    return redirect(caixa)

def cardapio(request):
    pedidoPronto = itemPedido.objects.filter(statusItem = 'p')
    pedidoAndamento = itemPedido.objects.filter(statusItem='a')
    pedidoCancelado = itemPedido.objects.filter(statusItem='c')

    context = {
        'produtos': produto.objects.all(),
        'prod': produto.objects.all(),
        'pedidoP': pedidoPronto,
        'pedidoA': pedidoAndamento,
        'pedidoC': pedidoCancelado,
        'itemPedidos': itemPedido.objects.all(),
    }

    return render(request, 'cardapio.html', context)

def esconderPedidoCardapio(request, id):
    #Pega o id do item Pedido
    esc = itemPedido.objects.get(id=id)
    #Altera o status do item pedido para l, para não aparecer na listagem
    esc.statusItem = 'l'
    esc.save()

    return redirect(cardapio)

def addItemPedido(request, id):
    if str(request.method) == 'POST':
        #Pega o id do produto
        produtoObj = produto.objects.get(id=id)
        produtoId = produtoObj.id
        valorUnitario = produtoObj.valorUnitario

        #Pega o input do tamplates e poe na variavel
        qtd = request.POST['quantidadeItemPedido']
        numeroMesa = request.POST['numeroMesa']

        #transformar o valorUnitario em decimal
        numMesa = int(numeroMesa)
        valorUni = float(valorUnitario)
        qtdNumber = float(qtd)

        #Calcular o valor do item pedido
        valorU = valorUni * qtdNumber

        validacaoMesa = False
        validacaoPedido = False

        while validacaoMesa == False:
            for mesas in mesa.objects.all():
                if  numMesa == mesas.numeroMesa and mesas.statusMesa == 'a':
                    mesaId = mesas.id
                    validacaoMesa = True
            
            if validacaoMesa == False:
                mesas = mesa(numeroMesa = numMesa, statusMesa = 'a')

                mesas.save()
                print(f'Mesa ae, numMesa{numMesa}, {mesas}')
                    
        while validacaoPedido == False:
            print('passou1')
            for pedidos in pedido.objects.all():
                if mesaId == pedidos.mesa_id:
                    pedidoId = pedidos.id
                    
                    print(f'{pedidoId}')
                    validacaoPedido = True

            if validacaoPedido == False:
                print('passou3')
                pedidos = pedido(dataPedido = '21:30', pessoa_id = 1, mesa_id = mesaId)

                print(f'Pedido ae, {pedidos.dataPedido}, {pedidos.mesa_id}')

                pedidos.save()

        #Fazer o create no bd
        print(f'PEDIDO AQ O {pedidoId}')
        item = itemPedido(quantidadeItemPedido = qtd, 
        pedido_id = pedidoId, 
        pessoa_id = 1, 
        produto_id = produtoId,
        statusItem = 'a', 
        valorItemPedido = valorU)

        #Salva no bd
        item.save()
    #item.pedido.mesa
    return redirect(cardapio)

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
    #Pega o id do item pedido
    pedidoC = itemPedido.objects.get(id=id)
    #Altera o status do item para cancelado
    pedidoC.statusItem = 'c'
    pedidoC.save()
    print('alohah cancelado')
    return redirect(cozinha)

def cozinhaPedidoPronto(request, id):
    #Pega o id do item pedido
    pedidoP = itemPedido.objects.get(id=id)
    #Altera o status do item para pronto
    pedidoP.statusItem = 'p'
    pedidoP.save()
    print('alohah pronto')
    return redirect(cozinha)


