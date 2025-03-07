from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProdutoViewSet, CondicaoPagamentoViewSet, PrecoViewSet
from django.urls import path, include  # Inclua o 'include' para o router
from .views import pagina_principal, gerar_relatorio, criar_pix, exibir_qr_code, gerar_pdf

# Definição das rotas do router
router = DefaultRouter()
router.register('clientes', ClienteViewSet)
router.register('produtos', ProdutoViewSet)
router.register('condicoes_pagamento', CondicaoPagamentoViewSet)
router.register('precos', PrecoViewSet)

# Combinação das rotas
urlpatterns = [
    path('', pagina_principal, name='pagina_principal'),  # Página principal
    path('relatorio/<int:cliente_id>/', gerar_relatorio, name='gerar_relatorio'),  # Relatório
    path('api/', include(router.urls)),  # Inclui as rotas do router com prefixo "api/"
    path('criar-pix/', criar_pix, name='criar_pix'),
    path('exibir-pix/', exibir_qr_code, name='exibir_pix'),
    path('gerar-pdf/<int:cliente_id>/', gerar_pdf, name='gerar_pdf'),
    path('gerar-pdf/<int:cliente_id>/', gerar_pdf, name='gerar_pdf'),
]
