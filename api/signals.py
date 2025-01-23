from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Preco
from .utils import verificar_alteracao_preco
import logging
from django.db.models.signals import pre_save

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Preco)
def notificar_alteracao_preco(sender, instance, **kwargs):
    """
    Sinal para verificar e notificar alterações de preço antes de salvar.
    """
    if instance.pk:  # Verifica se o objeto já existe no banco de dados (atualização)
        antigo_preco = sender.objects.get(pk=instance.pk).preco  # Obtém o preço antigo do banco
        novo_preco = instance.preco  # Novo preço sendo salvo

        logger.info(f"Produto '{instance.produto.descricao}' - Preço antigo: {antigo_preco}, Novo preço: {novo_preco}")

        if novo_preco < antigo_preco:
            logger.info(f"Preço reduzido detectado para '{instance.produto.descricao}'. Enviando notificação.")
            verificar_alteracao_preco(instance.produto, novo_preco)
        else:
            logger.info(f"Preço do produto '{instance.produto.descricao}' atualizado, mas não reduzido.")


