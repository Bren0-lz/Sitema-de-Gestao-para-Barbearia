from django.db import models

from django.core.exceptions import ValidationError
from django.utils import timezone

class Servico(models.Model):
    """
    Tabela de Serviços que a barbearia oferece.
    O Adm gerencia isso (Nome, Preço, Descrição).
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço (R$)")
    
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"

    class Meta:
        verbose_name = "Serviço"

# ... Classe Folga e HorarioDisponivel continuam iguais ...

class Agendamento(models.Model):
    # ... campos cliente_nome, cliente_telefone, data_hora ...

    # MUDANÇA DRASTICA AQUI:
    # Antes era: servico = models.CharField(...)
    # Agora é uma Chave Estrangeira (Ligação com a tabela Servico)
    servico = models.ManyToManyField(
        Servico, 
        verbose_name="Serviço Solicitado"
    )
    
class HorarioDisponivel(models.Model):
    """
    Representa um slot de tempo aberto pelo barbeiro.
    """
    data_hora = models.DateTimeField(verbose_name="Horário Disponível")
    reservado = models.BooleanField(default=False, verbose_name="Já Reservado?")

    def __str__(self):
        # CORREÇÃO AQUI:
        # Convertemos o horário UTC do banco para o fuso horário local (São Paulo)
        data_local = timezone.localtime(self.data_hora)
        
        status = "Reservado" if self.reservado else "Livre"
        # Usamos 'data_local' em vez de 'self.data_hora'
        return f"{data_local.strftime('%d/%m/%Y às %H:%M')} - {status}"

    class Meta:
        verbose_name = "Horário Disponível"
        verbose_name_plural = "Horários Disponíveis"
        ordering = ['data_hora']

class Agendamento(models.Model):
    """
    Representa a entidade principal do negócio: o horário marcado.
    Esta classe deve conter apenas dados e validações essenciais de domínio.
    """

    # Opções de Status (Evita "Magic Strings" no código)
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
    ]

    # Dados do Cliente
    cliente_nome = models.CharField(max_length=100, verbose_name="Nome do Cliente")
    cliente_telefone = models.CharField(max_length=20, verbose_name="Telefone")

    # Dados do Serviço
    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    servico = models.CharField(max_length=100, verbose_name="Serviço Solicitado")
    
    # Controle Interno
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    # ATUALIZE APENAS O MÉTODO CLEAN:
    def clean(self):
        """
        Regras de Validação (Programação Defensiva):
        1. Não permite agendamento no passado.
        2. Não permite choque de horários (Double Booking).
        """
        # Regra 1: Passado
        if self.data_hora and self.data_hora < timezone.now():
            raise ValidationError("Não é possível realizar agendamentos para o passado.")

        # Regra 2: Choque de Horário
        # Buscamos se existe (exists) algum agendamento com a MESMA data_hora
        # O .exclude(pk=self.pk) serve para permitir que você edite o próprio agendamento sem dar erro
        agendamento_conflitante = Agendamento.objects.filter(
            data_hora=self.data_hora
        ).exclude(pk=self.pk)

        if agendamento_conflitante.exists():
            raise ValidationError("Este horário já está ocupado. Por favor, escolha outro.")

    # Mantenha o save() e __str__ como estão...
    def save(self, *args, **kwargs):
        self.full_clean() # Força a validação antes de salvar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente_nome} - {self.data_hora.strftime('%d/%m %H:%M')}"

class Folga(models.Model):
    data_inicio = models.DateTimeField(verbose_name="Início da Folga")
    data_fim = models.DateTimeField(verbose_name="Fim da Folga")
    motivo = models.CharField(max_length=100, blank=True, verbose_name="Motivo (Opcional)")

    def clean(self):
        """
        Validação básica de datas.
        NOTA: Removemos a trava de clientes agendados. Agora é permitido salvar.
        """
        if self.data_inicio and self.data_fim:
            if self.data_inicio >= self.data_fim:
                raise ValidationError("A data final deve ser posterior à data inicial.")

    def save(self, *args, **kwargs):
        """
        Automação de Cancelamento em Massa:
        1. Identifica agendamentos no período.
        2. Deleta os agendamentos (e futuramente notifica).
        3. Deleta os horários disponíveis.
        """
        # 1. Valida datas
        self.full_clean()
        super().save(*args, **kwargs)

        # 2. Busca Agendamentos Conflitantes (Clientes reais)
        agendamentos_afetados = Agendamento.objects.filter(
            data_hora__gte=self.data_inicio,
            data_hora__lte=self.data_fim
        )

        # 3. Log e Exclusão dos Agendamentos
        if agendamentos_afetados.exists():
            print("="*50)
            print(f"⚠️  ALERTA DE FOLGA: {agendamentos_afetados.count()} CLIENTES CANCELADOS")
            print("="*50)
            
            for agendamento in agendamentos_afetados:
                # Aqui futuramente entrará o código do WhatsApp
                print(f"❌ Cancelando: {agendamento.cliente_nome} - {agendamento.cliente_telefone} - {agendamento.data_hora}")
                
                # Se quiser manter histórico, mude para: agendamento.status = 'CANCELADO'; agendamento.save()
                # Mas como você pediu para EXCLUIR:
                agendamento.delete() 
            
            print("="*50)

        # 4. Limpa os Slots de Horário (Livres ou Ocupados, todos somem)
        slots_para_remover = HorarioDisponivel.objects.filter(
            data_hora__gte=self.data_inicio,
            data_hora__lte=self.data_fim
        )
        slots_para_remover.delete()

    def __str__(self):
        return f"Bloqueio: {self.data_inicio.strftime('%d/%m %H:%M')} até {self.data_fim.strftime('%d/%m %H:%M')}"

    class Meta:
        verbose_name = "Folga / Bloqueio"
        verbose_name_plural = "Folgas / Bloqueios"