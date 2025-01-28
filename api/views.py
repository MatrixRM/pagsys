from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Cliente, Produto, CondicaoPagamento, Preco
from .serializers import ClienteSerializer, ProdutoSerializer, CondicaoPagamentoSerializer, PrecoSerializer
from .utils import verificar_alteracao_preco
import logging
from rest_framework.response import Response
from .utils import gerar_cobranca_pix




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


from django.shortcuts import render, get_object_or_404
from .models import Cliente, Preco

def gerar_relatorio(request, cliente_id):
    """
    Renderiza o relatório do cliente diretamente no navegador em formato HTML.
    """
    # Obter cliente e preços associados
    cliente = get_object_or_404(Cliente, id=cliente_id)
    precos = Preco.objects.filter(cliente=cliente)
    total_valor = sum(preco.preco for preco in precos)  # Calcula o valor total

    # Renderizar o template HTML
    context = {
        'cliente': cliente,
        'precos': precos,
        'total_valor': total_valor
    }
    return render(request, 'api/relatorio.html', context)









def criar_pix(request):
    """
    View para criar uma cobrança PIX.
    """
    valor = float(request.GET.get("valor", 0))
    descricao = request.GET.get("descricao", "Pagamento Teste")
    email = request.GET.get("email", "cliente@exemplo.com")

    try:
        resposta = gerar_cobranca_pix(valor, descricao, email)
        return JsonResponse({
            "message": "Cobrança PIX criada com sucesso!",
            "id": resposta["id"],
            "qr_code": resposta["point_of_interaction"]["transaction_data"]["qr_code"],
            "qr_code_base64": resposta["point_of_interaction"]["transaction_data"]["qr_code_base64"],
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



def exibir_qr_code(request):
    """
    Gera e exibe o QR Code para pagamento via PIX.
    """
    valor = float(request.GET.get("valor", 0))
    descricao = request.GET.get("descricao", "Pagamento Teste")
    email = request.GET.get("email", "robertomanica@yahoo.com.br")

    try:
        resposta = gerar_cobranca_pix(valor, descricao, email)
        return render(request, 'api/qr_code.html', {
            "qr_code_base64": resposta["point_of_interaction"]["transaction_data"]["qr_code_base64"],
            "qr_code": resposta["point_of_interaction"]["transaction_data"]["qr_code"],  # Código bruto do PIX
            "valor": valor,
            "descricao": descricao
        })
    except Exception as e:
        return render(request, 'api/erro.html', {"mensagem": str(e)})




def gerar_pdf(request, cliente_id):
    """
    Gera um PDF com os detalhes do relatório do cliente.
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)
    precos = Preco.objects.filter(cliente=cliente)
    total_valor = sum(preco.preco for preco in precos)

    # Renderizar o template como HTML
    template = get_template('api/relatorio_pdf.html')  # Template específico para PDF
    context = {
        'cliente': cliente,
        'precos': precos,
        'total_valor': total_valor
    }
    html = template.render(context)

    # Criar o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_{cliente.razao_social}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        logger.error(f"Erro ao gerar o PDF para o cliente {cliente.razao_social}")
        return HttpResponse('Erro ao gerar o PDF', status=500)

    return response
