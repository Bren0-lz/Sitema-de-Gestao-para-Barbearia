# api_barbeiro/serializers.py
from rest_framework import serializers
from core.models import Agendamento, HorarioDisponivel

class AgendamentoSerializer(serializers.ModelSerializer):
    """
    Responsável por converter objetos Agendamento em JSON e vice-versa.
    Seguindo o princípio de interface explícita.
    """
    class Meta:
        model = Agendamento
        # Definimos exatamente quais campos o App vai receber.
        # Isso evita vazar dados sensíveis ou desnecessários (Over-fetching).
        fields = [
            'id',
            'cliente_nome',
            'cliente_telefone',
            'data_hora',
            'servico',
            'status'
        ]

class HorarioDisponivelSerializer(serializers.ModelSerializer):
    """
    Permite que o App do Barbeiro leia e crie novos slots de tempo.
    """
    # Campo calculado para facilitar o frontend do app (exibe "12/12 - 14:00")
    titulo_legivel = serializers.SerializerMethodField()

    class Meta:
        model = HorarioDisponivel
        fields = ['id', 'data_hora', 'reservado', 'titulo_legivel']

    def get_titulo_legivel(self, obj):
        return obj.data_hora.strftime('%d/%m às %H:%M')