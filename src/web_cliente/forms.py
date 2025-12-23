# web_cliente/forms.py
from django import forms
from django.utils import timezone
from core.models import Agendamento, HorarioDisponivel, Servico # Importe Servico

class AgendamentoForm(forms.ModelForm):
    # Campo de Horário (Já configurado)
    horario_selecionado = forms.ModelChoiceField(
        queryset=HorarioDisponivel.objects.filter(reservado=False, data_hora__gte=timezone.now()),
        label="Escolha um Horário Disponível",
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="-- Selecione um horário --"
    )

    # Campo de Serviços Múltiplos
    servicos = forms.ModelMultipleChoiceField(
        queryset=Servico.objects.all(),
        label="Selecione os Serviços",
        # O widget CheckboxSelectMultiple permite marcar vários
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'btn-check'}), 
    )

    class Meta:
        model = Agendamento
        # Note o 's' no final de servicos
        fields = ['cliente_nome', 'cliente_telefone', 'servicos']
        
        widgets = {
            'cliente_nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu Nome'}),
            'cliente_telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) 9XXXX-XXXX'}),
            # Removemos o widget antigo de 'servico' pois definimos acima
        }