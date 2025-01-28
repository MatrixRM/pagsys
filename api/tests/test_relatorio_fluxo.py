import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from api.models import Cliente, Preco, Produto

class RelatorioE2ETest(LiveServerTestCase):
    def setUp(self):
        """Configuração inicial do navegador e criação de dados de teste"""
        self.browser = webdriver.Chrome()
        
        # Criando dados para o teste
        self.cliente = Cliente.objects.create(cnpj="12345678000123", razao_social="Cliente Teste")
        self.produto = Produto.objects.create(sku="001", descricao="Produto Teste")
        self.preco = Preco.objects.create(cliente=self.cliente, produto=self.produto, preco=100.00)

    def tearDown(self):
        """Fecha o navegador ao final do teste"""
        self.browser.quit()

    def test_relatorio_fluxo(self):
        """Teste fim a fim para gerar e visualizar um relatório"""

        try:
            # Acessa a página do relatório do cliente
            url = f"{self.live_server_url}/relatorio/{self.cliente.id}/"
            print(f"Acessando URL: {url}")  # Debug
            self.browser.get(url)

            # Aguarda um tempo extra para garantir o carregamento da página
            time.sleep(5)

            # Verifica se o título da página contém "Relatório"
            print(f"Título da página: {self.browser.title}")  # Debug
            self.assertTrue("Relatório" in self.browser.title, "Título da página não corresponde ao esperado.")

            # Aguarda um tempo extra antes de verificar os dados
            time.sleep(3)

            # Verifica se o nome do cliente está na página
            print("Verificando presença do Cliente...")
            self.assertIn(self.cliente.razao_social, self.browser.page_source)

            # Aguarda um tempo extra antes de verificar o produto
            time.sleep(2)

            # Verifica se o nome do produto está na página
            print("Verificando presença do Produto...")
            self.assertIn(self.produto.descricao, self.browser.page_source)

            # Obtém o preço correto da tabela Preco
            preco = Preco.objects.get(cliente=self.cliente, produto=self.produto).preco
            preco_formatado = f"R$ {preco:.2f}"  # Mantém o formato com ponto


            # Aguarda um tempo extra antes de verificar o preço
            time.sleep(3)

            # Depuração: imprime o preço formatado para verificar
            print(f"Preço esperado: {preco_formatado}")

            # Verifica se o preço está presente na página
            self.assertIn(preco_formatado, self.browser.page_source)
            print("Preço encontrado na página.")  # Debug

        except Exception as e:
            print(f"Erro durante o teste: {e}")  # Debugging
            raise  # Relevanta o erro para exibição no console
