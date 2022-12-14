# Generated by Django 4.1.3 on 2022-12-14 00:37

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import sistema.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('telefone', models.CharField(max_length=15, verbose_name='telefone')),
                ('funcao', models.CharField(max_length=12, verbose_name='Fun????o')),
                ('is_staff', models.BooleanField(default=True, verbose_name='Membro da equipe')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', sistema.models.UsuarioManager()),
            ],
        ),
        migrations.CreateModel(
            name='categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomeCategoria', models.CharField(max_length=50, verbose_name='nome')),
            ],
        ),
        migrations.CreateModel(
            name='mesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroMesa', models.IntegerField(verbose_name='numeroMesa')),
                ('statusMesa', models.CharField(max_length=2, verbose_name='statusMesa')),
            ],
        ),
        migrations.CreateModel(
            name='produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomeProduto', models.CharField(max_length=45, verbose_name='nome')),
                ('descricaoProduto', models.CharField(max_length=90, verbose_name='descricao')),
                ('valorUnitario', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='valor')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataPedido', models.TimeField(verbose_name='dataHoraPedido')),
                ('valorPedido', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='valorPedido')),
                ('porcentagemPedido', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='porcentagemPedido')),
                ('subTotalPedido', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='subTotalPedido')),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.mesa')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formaPagamento', models.CharField(max_length=9, verbose_name='formaPagamento')),
                ('dataPagamento', models.DateField(verbose_name='dataPagamento')),
                ('valorPagamento', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='valorPagamento')),
                ('valorPagamentoSubTotal', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='valorPagamentoSubTotal')),
                ('valorPagamentoServico', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='valorPagamentoServico')),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.mesa')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.pedido')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='itemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valorItemPedido', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='valorItemPedido')),
                ('quantidadeItemPedido', models.IntegerField(verbose_name='quantidadeItemPedido')),
                ('statusItem', models.CharField(max_length=5, verbose_name='statusItemPedido')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.produto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
