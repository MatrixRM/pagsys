from django.test import TestCase
from django.urls import reverse
from api.models import Cliente, Preco, Produto

class RelatorioViewTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(cnpj="12345678000123", razao_social="Cliente Teste")
        self.produto = Produto.objects.create(sku="001", descricao="Produto Teste")
        Preco.objects.create(cliente=self.cliente, produto=self.produto, preco=100.00)

    def test_relatorio_view(self):
        """Teste para verificar se a view de relatório funciona"""
        url = reverse('gerar_relatorio', args=[self.cliente.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cliente Teste")
        self.assertContains(response, "Produto Teste")
