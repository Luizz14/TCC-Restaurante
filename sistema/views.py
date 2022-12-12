from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic import RedirectView
from datetime import datetime

from .models import produto, itemPedido, mesa, pessoa, pedido, pagamento, categoria
from decimal import Decimal

def login(request):
    return render(request, 'login.html')

def caixa(request):
        #print(f'Valor da Mesa: {valoresMesas}')

        # qtd = itemPedidos.quantidadeItemPedido
        # prod = itemPedidos.produto.valorUnitario
        # valorItem = itemPedidos.valorItemPedido

        # #Calcula o valor total dos item pedidos
        # valorItem = qtd * prod
        #print(f'Valor Item: {valorItem}')
        #valorItem.save()

        # #Armazena valor da tabela
        # valoresMesas = calcularMesa.valorTotal

    context = {
        'pedidos': pedido.objects.all(),
        'itemPedidos': itemPedido.objects.all(),
        'produtos': produto.objects.all(),
        'categorias': categoria.objects.all(),
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

def retirarServico(request, id):
    
    objPedido = pedido.objects.get(id=id)
    objPedido.retirarServico()
    objPedido.save()

    return redirect(caixa)

def retirarItem(request, id):
    objItemPedido = itemPedido.objects.get(id=id)

    objPedido = pedido.objects.get(id=objItemPedido.pedido_id)
    if objItemPedido.quantidadeItemPedido > 1:
        objItemPedido.retirarItemPedido(1)
        objItemPedido.save()
    else:
        objItemPedido.delete()

    objPedido.retirarItemPedido(10, objItemPedido.valorItemPedido)        
    objPedido.save()

    #Excluir mesa caso não tenha mais nenhum pedido
    mesaBool = False
    for item in itemPedido.objects.all():
        if item.pedido_id == objItemPedido.pedido_id:
            mesaBool = True

    if mesaBool == False:
        mesaId = objItemPedido.pedido.mesa_id
        mesaObj = mesa.objects.get(id=mesaId)

        mesaObj.statusMesa = 'f'
        mesaObj.save()

    return redirect(caixa)

def addProduto(request):
    nomeProd = request.POST['nomeProdInput']
    descProd = request.POST['descProduto']
    valorProd = request.POST['valorProduto']
    categoriaProd = request.POST['categoriaProd']

    prod = produto(nomeProduto = nomeProd,
    descricaoProduto = descProd,
    valorUnitario = float(valorProd),
    categoria_id = int(categoriaProd))

    prod.save()

    return redirect(caixa)

def addFuncionario(request):
    nomeFunc = request.POST['nomeFuncionario']
    cpfFunc = request.POST['cpfFuncionario']
    senhaFunc = request.POST['senhaFuncionario']
    telefoneFunc = request.POST['telefoneFuncionario']
    funcaoFunc = request.POST['tipoFuncionario']

    func = pessoa(nome = nomeFunc,
    cpf = cpfFunc,
    senha = senhaFunc,
    telefone = int(telefoneFunc),
    tipo = funcaoFunc)

    func.save()

    return redirect(caixa)

def addCategoria(request):
    nomeCat = request.POST['nomeCategoria']
    cat = categoria(nomeCategoria = nomeCat)
    cat.save()

    return redirect(caixa)

def alterarMesa(request):
    numeroMesa = request.POST['numAtual']
    proxNumeroMesa = request.POST['numFuturo']

    validacaoMesa = False
    mensagem = 'Mesa movida com sucesso!'

    #Verificar se a mesa futura ja existe
    for objMesa in mesa.objects.all():
        if int(proxNumeroMesa) == objMesa.numeroMesa and objMesa.statusMesa == 'a':
            mensagem = 'A mesa ja existe!'
            validacaoMesa = True

    #Localiza onde esta a mesa atual para fazer o update
    for objMesa in mesa.objects.all():
        if int(numeroMesa) == objMesa.numeroMesa and objMesa.statusMesa == 'a' and validacaoMesa == False:

            objMesa.numeroMesa = int(proxNumeroMesa)
            objMesa.save()

    return redirect(caixa)

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
        print(f'Valor {objPedido}, {objPedido.valorPedido}')

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

    pedidoC.save()

    return redirect(cozinha)

def cozinhaPedidoPronto(request, id):
    #Pega o id do item pedido
    pedidoP = itemPedido.objects.get(id=id)
    #Altera o status do item para pronto
    pedidoP.statusItem = 'p'

    pedidoP.save()

    return redirect(cozinha)


