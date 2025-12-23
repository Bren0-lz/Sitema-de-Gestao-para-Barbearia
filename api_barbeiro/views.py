from django.shortcuts import render
from rest_framework import viewsets
from core.models import Agendamento, HorarioDisponivel
from .serializers import AgendamentoSerializer, HorarioDisponivelSerializer

class AgendamentoViewSet(viewsets.ModelViewSet):
    """
    Endpoint principal para o aplicativo da equipe.
    Permite visualizar, criar e editar agendamentos via API.
    """
    # Define de onde vêm os dados (QuerySet)
    queryset = Agendamento.objects.all().order_by('data_hora')
    
    # Define quem faz a tradução (Serializer)
    serializer_class = AgendamentoSerializer

class HorarioDisponivelViewSet(viewsets.ModelViewSet):
    """
    Endpoint para gestão de disponibilidade.
    O app do barbeiro vai mandar um POST aqui para abrir a agenda.
    """
    # Mostra primeiro os horários futuros
    queryset = HorarioDisponivel.objects.all().order_by('data_hora')
    serializer_class = HorarioDisponivelSerializer