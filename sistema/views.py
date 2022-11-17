from django.shortcuts import render

from .models import produto

def login(request):
    return render(request, 'login.html')

def caixa(request):
    return render(request, 'caixa.html')

def cozinha(request):
    return render(request, 'cozinha.hmtl')

def garcom(request):
    produtos = produto.objects.all()

    context = {
        'prod': produtos
    }
    return render(request, 'garcom.html', context)