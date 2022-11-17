from django.contrib import admin

from .models import produto

@admin.register(produto)
class produtoAdmin(admin.ModelAdmin):
    list_display = ('nomeProduto', 'descicaoProduto', 'valorUnitario', 'categoriaProduto')