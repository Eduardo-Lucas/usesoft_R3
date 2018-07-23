from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse

SIM_NAO_CHOICES = (('S', 'Sim'), ('N', 'Não'))


# Create your models here.


class UserProfile(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, default='')
    apelido = models.CharField(max_length=50, default='', null=True, blank=True)
    endereco = models.CharField(max_length=50, default='', null=True, blank=True)
    complemento = models.CharField(max_length=50, default='', null=True, blank=True)
    cep = models.IntegerField(default=0, null=True, blank=True)
    bairro = models.CharField(max_length=30, default='Bairro')
    cidade = models.CharField(max_length=50, default='Cidade')
    uf = models.CharField(max_length=2, default='BA', null=True, blank=True)
    # Login e Senha vem da tabela User
    nivel_acesso = models.IntegerField(default=0)
    supervisor = models.BooleanField(default=False)
    segunda_feira = models.BooleanField(default=True)
    segunda_hora_inicio = models.TimeField(default='8:00', blank=True, null=True)
    segunda_hora_final = models.TimeField(default='17:00', blank=True, null=True)
    terca_feira = models.BooleanField(default=True)
    terca_hora_inicio = models.TimeField(default='8:00', blank=True, null=True)
    terca_hora_final = models.TimeField(default='17:00', blank=True, null=True)
    quarta_feira = models.BooleanField(default=True)
    quarta_hora_inicio = models.TimeField(default='8:00', blank=True, null=True)
    quarta_hora_final = models.TimeField(default='17:00', blank=True, null=True)
    quinta_feira = models.BooleanField(default=True)
    quinta_hora_inicio = models.TimeField(default='8:00', blank=True, null=True)
    quinta_hora_final = models.TimeField(default='17:00', blank=True, null=True)
    sexta_feira = models.BooleanField(default=True)
    sexta_hora_inicio = models.TimeField(default='8:00', blank=True, null=True)
    sexta_hora_final = models.TimeField(default='17:00', blank=True, null=True)
    sabado = models.BooleanField(default=True)
    sabado_hora_inicio = models.TimeField(default='8:00', blank=True, null=True)
    sabado_hora_final = models.TimeField(default='17:00', blank=True, null=True)
    domingo = models.BooleanField(default=False)
    domingo_hora_inicio = models.TimeField(default='8:00', blank=True, null=True)
    domingo_hora_final = models.TimeField(default='17:00', blank=True, null=True)
    opera_caixa = models.BooleanField(default=False)
    numero_checkout = models.IntegerField(null=True, default=0)
    comprador = models.BooleanField(default=False)
    limite_por_compra = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    limite_compra = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    funcionario = models.CharField(max_length=3, choices=SIM_NAO_CHOICES, default='Sim')
    vendedor = models.CharField(max_length=3, choices=SIM_NAO_CHOICES, default='Não')
    codigo_supervisor = models.IntegerField(null=True, default=0)  # Auto relacionamento
    comissao_venda = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    comissao_sobre_servicos = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    objetivo_mensal_vendas = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    banco_numero = models.IntegerField(null=True, default=0)
    banco_agencia = models.IntegerField(null=True, default=0)
    banco_digito_verficador = models.IntegerField(null=True, default=0)
    data_nascimento = models.DateField(null=True, blank=True, default='2009-12-31')
    regiao_venda = models.CharField("Região de Venda", max_length=13, default='', blank=True, null=True)
    departamento = models.CharField(max_length=15, default='', blank=True, null=True)
    matricula = models.CharField(max_length=20, default='', blank=True, null=True)
    # Grupo vem da tabela User
    identidade = models.CharField(max_length=20, blank=True, null=True)
    data_emissao = models.DateField(blank=True, null=True, default='2009-12-31')
    orgao_emissor = models.CharField(max_length=10, blank=True, null=True)
    fisica_juridica = models.CharField(max_length=1, default='F')
    cpf_cnpj = models.IntegerField(default=0)
    sexo = models.CharField(max_length=1, default='M')
    ddd_residencia = models.IntegerField(null=True, default=0)
    tel_residencia = models.IntegerField(null=True, default=0)
    ddd_celular = models.IntegerField(null=True, default=0)
    tel_celular = models.IntegerField(null=True, default=0)
    informacoes_adicionais = models.TextField(max_length=256, default='', blank=True, null=True)
    email = models.EmailField(max_length=50, default='usuario@email.com')

    def get_absolute_url(self):
        return reverse('acc:userprofile-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuário'


"""
    SIGNALS
"""


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(usuario=kwargs['instance'])


post_save.connect(create_profile, sender=User)
