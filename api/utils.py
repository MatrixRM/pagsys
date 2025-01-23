from twilio.rest import Client
from django.conf import settings
from .models import Preco
import logging



logger = logging.getLogger(__name__)

def enviar_notificacao(celular_cliente, mensagem):
    """
    Envia uma notificação SMS para o cliente utilizando Twilio.
    """
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=mensagem,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=celular_cliente
        )
        logger.info(f"Mensagem enviada com sucesso para {celular_cliente}: SID {message.sid}")
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem para {celular_cliente}: {e}")


def verificar_alteracao_preco(produto, novo_preco):
    """
    Verifica se o novo preço do produto é menor que o preço registrado anteriormente.
    Caso seja, envia uma notificação para o cliente associado.
    """
    logger.info(f"Verificando alterações de preço para o produto: {produto.descricao}, novo preço: R$ {novo_preco:.2f}")
    precos_antigos = Preco.objects.filter(produto=produto)

    for preco_antigo in precos_antigos:
        logger.info(f"Cliente: {preco_antigo.cliente.razao_social}, Preço antigo: R$ {preco_antigo.preco:.2f}")
        if novo_preco < preco_antigo.preco:
            mensagem = (
                f"Olá {preco_antigo.cliente.razao_social}, o preço do produto "
                f"'{produto.descricao}' foi reduzido para R$ {novo_preco:.2f}, "
                f"inferior ao valor que você adquiriu anteriormente (R$ {preco_antigo.preco:.2f})."
            )
            if preco_antigo.cliente.celular:
                logger.info(f"Enviando notificação para {preco_antigo.cliente.razao_social} ({preco_antigo.cliente.celular}).")
                enviar_notificacao(preco_antigo.cliente.celular, mensagem)
            else:
                logger.warning(f"Cliente {preco_antigo.cliente.razao_social} não possui celular cadastrado.")



