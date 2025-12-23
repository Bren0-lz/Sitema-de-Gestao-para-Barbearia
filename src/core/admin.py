# core/admin.py
from django.contrib import admin
from django.contrib import messages
from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .models import Agendamento, HorarioDisponivel, Folga
from .services import gerar_horarios_proximos_dias
from .models import Agendamento, HorarioDisponivel, Folga, Servico # Importe Servico

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco')
    search_fields = ('nome',)
    
@admin.register(Folga)
class FolgaAdmin(admin.ModelAdmin):
    list_display = ('data_inicio', 'data_fim', 'motivo')

@admin.action(description='📅 Gerar Agenda Anual (365 dias)')
def acao_gerar_agenda_anual(self, request, queryset):
    qtd = gerar_horarios_proximos_dias(dias=365)
    self.message_user(request, f"Sucesso Massivo! {qtd} horários criados para o ano todo.", messages.SUCCESS)

@admin.register(HorarioDisponivel)
class HorarioDisponivelAdmin(admin.ModelAdmin):
    # ADICIONE ESTA LINHA: Força o Django a usar nosso HTML
    change_list_template = "admin/core/lista_horarios_admin.html"
    
    list_display = ('data_hora', 'reservado')
    list_filter = ('reservado', 'data_hora')

    # ... (mantenha o get_urls e gerar_agenda_view como já fizemos) ...
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('gerar_agenda/', self.gerar_agenda_view),
        ]
        return my_urls + urls

    def gerar_agenda_view(self, request):
        # Atualizei para gerar 365 dias conforme seu pedido anterior
        from .services import gerar_horarios_proximos_dias
        qtd = gerar_horarios_proximos_dias(dias=365)
        
        if qtd > 0:
            self.message_user(request, f"Sucesso! {qtd} novos horários criados.", messages.SUCCESS)
        else:
            self.message_user(request, "Nenhum horário novo (talvez já existam ou seja folga).", messages.WARNING)
        
        return HttpResponseRedirect("../")
    
@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente_nome', 'data_hora', 'servico', 'status')