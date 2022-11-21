from django.shortcuts import render

from .models import produto, itemPedido, mesa, pessoa, pedido, pagamento

def login(request):
    return render(request, 'login.html')

def caixa(request):

    context = {
        'pedidos': pedido.objects.all(),
        'mesas': mesa.objects.all(),
        'itemPedidos': itemPedido.objects.all()
    }

    return render(request, 'caixa.html', context)

def cozinha(request):
    pedidoPronto = itemPedido.objects.filter(statusItem = 'p')
    #pedidoPronto = produto.objects.exclude(categoriaProduto = 'Bebida')

    pedidoAndamento = produto.objects.exclude(categoriaProduto = 'Bebida')
    pedidoAndamento = itemPedido.objects.filter(statusItem='a')

    buttonPronto = itemPedido.objects.get(statusItem = 'p')
    #buttonPronto.save()
    context = {
        'pedidoP': pedidoPronto,
        'pedidoA': pedidoAndamento,
    }

    return render(request, 'cozinha.html', context)



def cardapio(request):
    produtos = produto.objects.all()
    
    """
    almoco = produto.objects.filter(categoriaProduto = 'Almoço')
    pedidoPronto = itemPedido.objects.filter(statusItem = 'p')
    pedidoAndamento = itemPedido.objects.filter(statusItem='a')
    pedidoCancelado = itemPedido.objects.filter(statusItem='c')
    """


    context = {
        'prod': produtos,
    }


    return render(request, 'cardapio.html', context)

def inserir(request):

    #if request.method == 'POST':
        #form = forms.Inserir(request.POST)
        #if

    m = request.POST.get('numeroMesa')
    mesa.objects.create(numeroMesa = m)
    
    #m.save()

    q = request.POST.get('quantidadeItemPedido')

    qtd = request.POST.get('quantidadeItemPedido')
    itemPedido.objects.create(quantidadeItemPedido = qtd)    
    
    itemPedido.objects.create(statusItem = 'e')
    itemPedido.objects.create(valorItemPedido = qtd)
    itemPedido.objects.create(pedido_id = 2)
    itemPedido.objects.create(pessoa_id = 1)
    itemPedido.objects.create(produto_id = 4)
    
    itemPedido.save()

    return render(cardapio)
