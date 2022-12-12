from django.shortcuts import render, redirect
from django.http import JsonResponse

from ..models import pedido, mesa

def listarTodosPedidos(request):
    # return 'hello world'
    # return render(request, 'caixa.html')

    objPedidos = pedido.objects.all().values()

    return JsonResponse({"objPedidos": list(objPedidos)})

def listarPedidosPor(request):
    # return 'hello world'
    # return render(request, 'caixa.html')

    # filterPedido = lambda statusMesa: statusMesa == 'a'
    # objPedidos = pedido.objects.filter(filterPedido(objMesa.statusMesa)).values()
    
    # Testes Pedido -> Mesa
    # objPedidos = pedido.objects.all().values() #.objects.first()
    #print('Aqui1: ', objPedidos)

    objPedidosFiltrados = pedido.mesas.objects.filter(statusMesa = 'a').values()

    # objPedidosFiltrados = objPedidos.mesa.filter(statusMesa = 'a').values()


    # Testes no objeto mesa
    objMesa = mesa.objects.filter(statusMesa = 'a').values()
    #idMesa = objMesa.id
    
    print(f'2 - Mesa id: {list(objMesa)}')

    # Escolher os campos da lista a exibir
    newObjMesa = []
    for x in list(objMesa):
        newObjMesa.append(x["id"])

    print(f'3 - Mesas ids: {newObjMesa}')




    return JsonResponse({"objPedidos": list(objPedidosFiltrados)})
    # return JsonResponse({"objPedidos": list(objPedidosFiltrados)})