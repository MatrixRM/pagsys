from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Cliente, Produto, CondicaoPagamento, Preco
from .serializers import ClienteSerializer, ProdutoSerializer, CondicaoPagamentoSerializer, PrecoSerializer
from .utils import enviar_notificacao, verificar_alteracao_preco
import logging
from rest_framework.response import Response

# Configuração de logging
logger = logging.getLogger(__name__)

# ViewSets para API REST
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class CondicaoPagamentoViewSet(viewsets.ModelViewSet):
    queryset = CondicaoPagamento.objects.all()
    serializer_class = CondicaoPagamentoSerializer



class PrecoViewSet(viewsets.ModelViewSet):
    queryset = Preco.objects.all()
    serializer_class = PrecoSerializer

    def update(self, request, *args, **kwargs):
        # Obter a instância do preço
        instance = self.get_object()
        antigo_preco = instance.preco
        novo_preco = float(request.data.get('preco', instance.preco))

        logger.info(f"Alterando o preço do produto '{instance.produto.descricao}' de R$ {antigo_preco:.2f} para R$ {novo_preco:.2f}")

        # Verificar se o preço foi reduzido
        if novo_preco < antigo_preco:
            logger.info(f"Preço reduzido detectado para o produto '{instance.produto.descricao}'. Chamando função de verificação.")
            verificar_alteracao_preco(instance.produto, novo_preco)
        else:
            logger.info(f"Preço do produto '{instance.produto.descricao}' não foi reduzido. Nenhuma ação necessária.")

        # Atualizar o preço no banco de dados
        instance.preco = novo_preco
        instance.save()

        # Retornar a resposta serializada
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)



# Página Principal
def pagina_principal(request):
    clientes = None
    if 'search' in request.GET:
        termo = request.GET.get('search')
        clientes = Cliente.objects.filter(razao_social__icontains=termo) | Cliente.objects.filter(cnpj__icontains=termo)
    
    context = {'clientes': clientes}
    return render(request, 'api/pagina_principal.html', context)


# Gerar Relatório em PDF
def gerar_relatorio(request, cliente_id):
    # Obter cliente e preços associados
    cliente = get_object_or_404(Cliente, id=cliente_id)
    precos = Preco.objects.filter(cliente=cliente)

    # Renderizar o template HTML
    template = get_template('api/relatorio.html')
    context = {'cliente': cliente, 'precos': precos}
    html = template.render(context)

    # Gerar o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_{cliente.razao_social}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Verificar erros na geração do PDF
    if pisa_status.err:
        logger.error("Erro ao gerar o PDF para o cliente %s", cliente.razao_social)
        return HttpResponse('Erro ao gerar o PDF', status=500)

    logger.info("PDF gerado com sucesso para o cliente %s", cliente.razao_social)
    return response
