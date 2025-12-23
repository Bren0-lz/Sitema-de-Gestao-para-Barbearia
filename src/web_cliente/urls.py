# web_cliente/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.realizar_agendamento, name='realizar_agendamento'),
    # Nova rota para o HTMX
    path('ajax/carregar-horarios/', views.carregar_horarios, name='ajax_carregar_horarios'),
]