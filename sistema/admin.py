from django.contrib import admin
from .models import produto, usuario
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import usuario
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUsuarioCreateForm, CustomUsuarioChangeForm

@admin.register(produto)
class produtoAdmin(admin.ModelAdmin):
    list_display = ('nomeProduto', 'descricaoProduto', 'valorUnitario')



@admin.register(usuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form = CustomUsuarioChangeForm
    model = usuario
    list_display = ('first_name', 'last_name', 'email', 'telefone', 'is_staff', 'funcao')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'telefone', 'funcao')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

