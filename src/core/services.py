# core/services.py
from datetime import timedelta
from django.utils import timezone
from .models import HorarioDisponivel, Folga

def gerar_horarios_proximos_dias(dias=7):
    """
    Gera slots de 30 min, das 09:00 às 18:00, Seg-Sex.
    Respeita as regras de Folga e Fuso Horário Local.
    """
    # Configurações do Negócio
    HORA_INICIO = 9
    HORA_FIM = 18
    INTERVALO_MINUTOS = 30
    
    # [CORREÇÃO CRÍTICA DE TIMEZONE]
    # 1. Pegamos o fuso horário definido no settings (America/Sao_Paulo)
    tz_local = timezone.get_current_timezone()
    
    # 2. Pegamos o "agora" e forçamos ele a ser "agora em São Paulo"
    agora = timezone.now().astimezone(tz_local)
    
    # 3. Zeramos as horas para começar a contagem do início do dia
    data_atual = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    
    novos_horarios = []

    for i in range(dias):
        # Avança dia por dia (mantendo o fuso horário correto)
        dia_analise = data_atual + timedelta(days=i)

        # Regra 1: Pula Sábado (5) e Domingo (6)
        if dia_analise.weekday() > 4:
            continue

        # Loop das horas dentro do dia
        # Aqui garantimos que o horário criado já nasça com o fuso correto
        horario_cursor = dia_analise.replace(hour=HORA_INICIO)
        horario_limite = dia_analise.replace(hour=HORA_FIM)

        while horario_cursor <= horario_limite:
            # Regra 2: Verifica se já existe (Duplicidade)
            if not HorarioDisponivel.objects.filter(data_hora=horario_cursor).exists():
                
                # Regra 3: Verifica se é Folga
                eh_folga = Folga.objects.filter(
                    data_inicio__lte=horario_cursor,
                    data_fim__gte=horario_cursor
                ).exists()

                if not eh_folga:
                    novos_horarios.append(HorarioDisponivel(data_hora=horario_cursor))
            
            # Avança 30 minutos
            horario_cursor += timedelta(minutes=INTERVALO_MINUTOS)

    HorarioDisponivel.objects.bulk_create(novos_horarios)
    return len(novos_horarios)