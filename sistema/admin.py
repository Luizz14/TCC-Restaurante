from django.contrib import admin
from .models import produto, pessoa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

@admin.register(produto)
class produtoAdmin(admin.ModelAdmin):
    list_display = ('nomeProduto', 'descricaoProduto', 'valorUnitario')

# @admin.register(pessoa)
# class pessoaAdmin(admin.ModelAdmin):
#     list_display = ('nome', 'cpf', 'senha', 'telefone', 'tipo', 'user')



# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# class pessoaInline(admin.StackedInline):
#     model = pessoa
#     can_delete = False
#     verbose_name_plural = 'pessoa'

# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (pessoaInline,)

# # Re-register UserAdmin
# admin.site.unregister(pessoa)
# admin.site.register(pessoa, UserAdmin)
