from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse

from choices.models import SIM_NAO_CHOICES, FISICA_JURIDICA_CHOICES
from globais.models import Uf, Municipio, PaisIbge


# ---------------------------------------------------------------------------------------------------------------------
# grupos de clientes
# ---------------------------------------------------------------------------------------------------------------------
class GrupoParticipante(models.Model):
    codigo = models.CharField("Código do Grupo de participantes", unique=True, max_length=5)
    descricao = models.CharField("Descrição do Grupo de participantes", max_length=80)

    habilitado = models.CharField("Habilitado para uso", max_length=1, default="S",
                                  choices=SIM_NAO_CHOICES,
                                  help_text='Desabilite este Grupo caso sua empresa não o utilize ou utilize muito '
                                            'esporadicamente para evitar erros')
    ultima_alteracao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.codigo + " - " + self.descricao

    class Meta:
        ordering = ('descricao',)
        verbose_name = "Grupo de Participante"
        verbose_name_plural = "Grupos de Participantes"


# -----------------------------------------------------------------------------------------------------------------------
# regiões de vendas
# -----------------------------------------------------------------------------------------------------------------------
class RegiaoDeVenda(models.Model):
    codigo = models.CharField("Código da região de vendas", unique=True, max_length=5, null=False)
    descricao = models.CharField("Descrição da região de vendas", max_length=80, null=False)
    habilitado = models.CharField("Habilitado para uso", max_length=1, null=False, default="N",
                                  choices=SIM_NAO_CHOICES,
                                  help_text='Desabilite este CFOP caso sua empresa não o utilize ou utilize muito '
                                            'esporadicamente para evitar erros')
    ultima_alteracao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.codigo + " - "+self.descricao

    class Meta:
        ordering = ('descricao',)
        verbose_name = "Região de Venda"
        verbose_name_plural = "Regiões de Vendas"


# ----------------------------------------------------------------------------------------------------------------------
# códigos de participantes clientes ou fornecedores (kfai01)
# ----------------------------------------------------------------------------------------------------------------------
class Participante(models.Model):
    razao_social = models.CharField(max_length=50, blank=False)
    nome_fantasia = models.CharField("Nome Fantasia", max_length=50, blank=False)
    fisica_juridica = models.CharField("Pessoa Física(F) ou Jurídica (J)", max_length=1, blank=False,
                                       choices=FISICA_JURIDICA_CHOICES, default='J')
    cnpj_cpf = models.CharField("CNPJ/CPF", max_length=14, blank=True, null=True)
    inscricao_estadual = models.CharField("Inscricao Estadual", max_length=15, blank=False,
                                          default="ISENTO")
    inscricao_municipal = models.CharField("Inscrição Municipal", max_length=15,
                                           blank=True, default="ISENTO")

    # TODO Depois excluir a opção null=True
    codigo = models.PositiveIntegerField("Código", validators=[MaxValueValidator(99999999)], blank=True, null=True)

    vendedor = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="responsavel")

    # TODO 1. Depois excluir a opção null=True
    regiao_de_venda = models.ForeignKey(RegiaoDeVenda, on_delete=models.CASCADE, blank=True, null=True)
    # regiao_de_venda = models.IntegerField(blank=True, null=True)

    # TODO 2. Depois excluir a opção null=True
    grupo = models.ForeignKey(GrupoParticipante, on_delete=models.CASCADE, blank=True, null=True)

    endereco = models.CharField("Endereço", max_length=60, blank=True, null=True)
    complemento = models.CharField("Complemento", max_length=60, blank=True, null=True)
    numero = models.CharField("Número", max_length=10, blank=True, null=True)
    bairro = models.CharField("Bairro", max_length=10, blank=True, null=True)

    # TODO 3. Depois excluir a opção null=True
    cidade = models.ForeignKey(Municipio, on_delete=models.CASCADE, blank=True, null=True)
    # cidade = models.IntegerField(blank=True, null=True)

    cep = models.PositiveIntegerField("CEP", null=True, blank=True,
                                      validators=[MaxValueValidator(99999999)])

    # TODO 4. Depois excluir a opção null=True
    estado = models.ForeignKey(Uf, on_delete=models.CASCADE, blank=True, null=True)
    # estado = models.IntegerField(blank=True, null=True)

    # TODO 5. Depois excluir a opção null=True
    pais = models.ForeignKey(PaisIbge, on_delete=models.CASCADE, blank=True, null=True)
    # pais = models.IntegerField(blank=True, null=True)

    telefone = models.CharField("Telefone 1", max_length=20, blank=True, null=True)

    telefone2 = models.CharField("Telefone 2", max_length=20, blank=True, null=True)

    celular = models.CharField("Celular 1", max_length=20, blank=True, null=True)

    celular2 = models.CharField("Celular 2", max_length=20, blank=True, null=True)

    email = models.CharField("E-mail", max_length=40, blank=True, null=True)
    
    ultima_alteracao = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('faturamento:participante_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.razao_social)

    def exibe_complemento(self):
        if self.complemento:
            return self.complemento
        else:
            return "-"

    def exibe_bairro(self):
        if self.bairro:
            return self.bairro
        else:
            return "-"

    def exibe_telefone2(self):
        if self.telefone2:
            return self.telefone2
        else:
            return "-"

    def exibe_email(self):
        if self.email:
            return self.email
        else:
            return "Favor atualizar E-mail."

    def exibe_fisica_juridica(self):
        if self.fisica_juridica == 'J':
            return "Pessoa Jurídica"
        else:
            return "Pessoa Física"

    class Meta:
        ordering = ['razao_social']
        verbose_name = 'Cadastro de Participante'
        verbose_name_plural = 'Cadastro de Participantes'


# ---------------------------------------------------------------------------------------------------------------------
#  dados da nota fiscal
# ---------------------------------------------------------------------------------------------------------------------
class NotaFiscal(models.Model):
    numero_nfe = models.PositiveIntegerField("Número da Nota Fiscal", null=True, blank=True,
                                             validators=[MaxValueValidator(99999999)])
    serie_nfe = models.PositiveIntegerField("Série da Nota Fiscal", null=True, blank=True,
                                            validators=[MaxValueValidator(999)])
    subserie_nfe = models.PositiveIntegerField("SubSérie da Nota fiscal", null=True, blank=True,
                                               validators=[MaxValueValidator(999)])
    ultima_alteracao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.numero_nfe)

    class Meta:
        ordering = ['numero_nfe']
        verbose_name = 'Cadastro de notas fiscais emitidas e recebidas'
        verbose_name_plural = 'Cadastro de notas fiscais emitidas e recebidas'
