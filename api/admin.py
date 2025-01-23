from django.contrib import admin
from .models import Cliente, Produto, CondicaoPagamento, Preco

admin.site.register(Cliente)
admin.site.register(Produto)
admin.site.register(CondicaoPagamento)
admin.site.register(Preco)
