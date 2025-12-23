# web_cliente/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import HorarioDisponivel # <-- Importante
from .forms import AgendamentoForm

def realizar_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        
        if form.is_valid():
            # 1. Cria o objeto na memória (sem salvar no banco ainda)
            novo_agendamento = form.save(commit=False)
            
            horario_id = request.POST.get('horario_selecionado')
            
            if horario_id:
                try:
                    horario_obj = HorarioDisponivel.objects.get(id=horario_id)
                    novo_agendamento.data_hora = horario_obj.data_hora
                    
                    # 2. Salva o Agendamento (Gera o ID)
                    novo_agendamento.save()
                    
                    # 3. CRUCIAL: Agora que tem ID, salva os Serviços selecionados
                    form.save_m2m() 
                    
                    # 4. Queima o slot
                    horario_obj.reservado = True
                    horario_obj.save()
                    
                    messages.success(request, 'Agendamento confirmado com sucesso!')
                    return redirect('realizar_agendamento')
                except HorarioDisponivel.DoesNotExist:
                    messages.error(request, 'O horário selecionado não é válido.')
            else:
                messages.error(request, 'Por favor, selecione um horário no calendário.')
        else:
            messages.error(request, 'Erro ao agendar. Verifique os dados.')
    else:
        form = AgendamentoForm()

    return render(request, 'web_cliente/agendamento.html', {'form': form})

def carregar_horarios(request):
    """
    Retorna TODOS os horários do dia.
    O template vai decidir qual pintar de cinza (reservado) ou dourado (livre).
    """
    data_selecionada = request.GET.get('data')
    
    if data_selecionada:
        # MUDANÇA AQUI: Removemos o filtro 'reservado=False'
        # Trazemos tudo ordenado por hora
        horarios = HorarioDisponivel.objects.filter(
            data_hora__date=data_selecionada
        ).order_by('data_hora')
    else:
        horarios = []

    return render(request, 'web_cliente/lista_horarios.html', {'horarios': horarios})