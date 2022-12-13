from django.shortcuts import render, redirect
from datetime import date, datetime

from ..models import pedido, mesa, itemPedido, produto, categoria, pagamento, pessoa

def caixa(request):

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

    pagamentoForma = request.POST['pagamentoSelect']

    mesaId = pedidoId.mesa
    mesaId.statusMesa = 'f'

    dateNow = date.today()

    objPagamento = pagamento(
                                formaPagamento = pagamentoForma,
                                dataPagamento = dateNow,
                                valorPagamento = pedidoId.valorPedido,
                                valorPagamentoSubTotal = pedidoId.subTotalPedido,
                                valorPagamentoServico = pedidoId.porcentagemPedido,
                                pedido_id = pedidoId.id,
                                pessoa_id = 1,
                                mesa_id = mesaId.id,
                            )
    
    objPagamento.save()
    mesaId.save()

    return redirect(caixa)

def retirarServico(request, id):
    
    objPedido = pedido.objects.get(id=id)
    objPedido.retirarServico()

    #Salva no bd
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

    objPedido.retirarItemPedido(10, objItemPedido.produto.valorUnitario)        

    #Salva no bd
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

        #Salva no bd
        mesaObj.save()

    return redirect(caixa)

def addProduto(request):
    nomeProd = request.POST['nomeProdInput']
    descProd = request.POST['descProduto']
    valorProd = request.POST['valorProduto']
    categoriaProd = request.POST['categoriaProd']

    prod = produto(
                        nomeProduto = nomeProd,
                        descricaoProduto = descProd,
                        valorUnitario = float(valorProd),
                        categoria_id = int(categoriaProd)
                    )

    #Salva no bd
    prod.save()

    return redirect(caixa)

def addFuncionario(request):
    nomeFunc = request.POST['nomeFuncionario']
    cpfFunc = request.POST['cpfFuncionario']
    senhaFunc = request.POST['senhaFuncionario']
    telefoneFunc = request.POST['telefoneFuncionario']
    funcaoFunc = request.POST['tipoFuncionario']

    func = pessoa(
                    nome = nomeFunc,
                    cpf = cpfFunc,
                    senha = senhaFunc,
                    telefone = int(telefoneFunc),
                    tipo = funcaoFunc
                  )

    #Salva no bd
    func.save()

    return redirect(caixa)

def addCategoria(request):
    nomeCat = request.POST['nomeCategoria']
    cat = categoria(nomeCategoria = nomeCat)

    #Salva no bd
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
            
            #Salva no bd
            objMesa.save()

    return redirect(caixa)

def encerrarDia(request):
    dateNow = date.today()

    valorTotal = 0
    valorSubTotal = 0
    valorServico = 0
    valorTotalCartao = 0
    valorTotalDinheiro = 0
    valorTotalPix = 0

    for objPagamento in pagamento.objects.all():
        if objPagamento.dataPagamento == dateNow:
            valorTotal += objPagamento.valorPagamento
            valorSubTotal += objPagamento.valorPagamentoSubTotal
            valorServico += objPagamento.valorPagamentoServico

            if objPagamento.formaPagamento == 'Cartão':
                valorTotalCartao += objPagamento.valorPagamento

            if objPagamento.formaPagamento == 'Dinheiro':
                valorTotalDinheiro += objPagamento.valorPagamento

            if objPagamento.formaPagamento == 'Pix':
                valorTotalPix += objPagamento.valorPagamento

    context = {
        'dateTime': dateNow,
        'objPagamento': pagamento.objects.all(),
        'valorTotal': valorTotal,
        'valorTotalCartao': valorTotalCartao,
        'valorTotalDinheiro': valorTotalDinheiro,
        'valorTotalPix': valorTotalPix,
        'valorSubTotal': valorSubTotal,
        'valorServico': valorServico,
    }
    
    return render(request, 'encerramento.html', context)
