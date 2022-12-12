from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from datetime import datetime

from ..models import produto, itemPedido, mesa, pessoa, pedido, pagamento, categoria

def cardapio(request):
    pedidoPronto = itemPedido.objects.filter(statusItem = 'p')
    pedidoAndamento = itemPedido.objects.filter(statusItem= 'a')
    pedidoCancelado = itemPedido.objects.filter(statusItem= 'c')

    context = {
        'produtos': produto.objects.all(),
        'itemPedidos': itemPedido.objects.all(),
        'categorias': categoria.objects.all(),
        'pedidoP': pedidoPronto,
        'pedidoA': pedidoAndamento,
        'pedidoC': pedidoCancelado,
    }

    return render(request, 'cardapio.html', context)

def esconderPedidoCardapio(request, id):
    #Pega o id do item Pedido
    esc = itemPedido.objects.get(id=id)
    #Altera o status do item pedido para l, para não aparecer na listagem
    esc.statusItem = 'l'

    #Salva no bd
    esc.save()

    return redirect(cardapio)

def addItemPedido(request, id):
    if str(request.method) == 'POST':
        #Pega o id do produto
        produtoObj = produto.objects.get(id=id)
        produtoId = produtoObj.id
        valorUnitario = produtoObj.valorUnitario

        #Pega obj de pedido

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
                
                #Salva no bd
                mesas.save()

        while validacaoPedido == False:
            for pedidos in pedido.objects.all():
                if mesaId == pedidos.mesa_id:
                    pedidoId = pedidos.id

                    validacaoPedido = True

            if validacaoPedido == False:
                atual = datetime.now()
                horaAtual = atual.strftime("%H:%M")

                pedidos = pedido(
                                    dataPedido = horaAtual,
                                    pessoa_id = 1,
                                    mesa_id = mesaId,
                                    valorPedido = 0,
                                    porcentagemPedido = 0,
                                    subTotalPedido = 0,
                                )

                pedidos.save()

        objPedido = pedido.objects.get(id=pedidoId)
        objPedido.adicionarItemPedido(10, valorU)

        # objPedido.porcentagemPedido = valorTotal
        # valorPaoParametro = parametro.objects.get(nome='Pao').valor

        # objPedido.calcularPercentualServico(10)
        objPedido.save()

        #Fazer o create no bd
        item = itemPedido(
                            quantidadeItemPedido = qtd,
                            pedido_id = pedidoId,
                            pessoa_id = 1,
                            produto_id = produtoId,
                            statusItem = 'a',
                            valorItemPedido = valorU
                        )

        #Salva no bd
        item.save()

    return redirect(cardapio)
