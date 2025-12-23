# api_barbeiro/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgendamentoViewSet, HorarioDisponivelViewSet # <-- Importe o novo viewset

router = DefaultRouter()
router.register(r'agendamentos', AgendamentoViewSet)
router.register(r'horarios', HorarioDisponivelViewSet) # <-- Nova rota

urlpatterns = [
    path('', include(router.urls)),
]