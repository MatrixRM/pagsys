from django.test import TestCase
from api.models import Cliente

class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            cnpj="12345678000123",
            razao_social="Cliente Teste"
        )

    def test_cliente_razao_social(self):
        """Teste para verificar o nome do cliente"""
        self.assertEqual(self.cliente.razao_social, "Cliente Teste")

    def test_cliente_cnpj(self):
        """Teste para verificar o CNPJ do cliente"""
        self.assertEqual(self.cliente.cnpj, "12345678000123")
