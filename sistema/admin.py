from django.contrib import admin

from .models import produto, pessoa

@admin.register(produto)
class produtoAdmin(admin.ModelAdmin):
    list_display = ('nomeProduto', 'descricaoProduto', 'valorUnitario')

@admin.register(pessoa)
class pessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'senha', 'telefone', 'tipo')