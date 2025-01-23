from django.db import models

class Cliente(models.Model):
    cnpj = models.CharField(max_length=45, unique=True)
    razao_social = models.CharField(max_length=45)
    celular = models.CharField(max_length=15, blank=True, null=True)  # Novo campo para celular

    def __str__(self):
        return self.razao_social


class Produto(models.Model):
    sku = models.CharField(max_length=45, unique=True)
    descricao = models.CharField(max_length=45)

    def __str__(self):
        return self.descricao

class CondicaoPagamento(models.Model):
    descricao = models.CharField(max_length=45)
    dias = models.PositiveIntegerField()

    def __str__(self):
        return self.descricao

class Preco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cliente} - {self.produto}: {self.preco}"
