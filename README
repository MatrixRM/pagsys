# PagSys

Sistema de Pagamentos com Notificação Automática via SMS utilizando Django e Twilio.

---

## Descrição

O **PagSys** é uma aplicação web desenvolvida em Django para gerenciar clientes, produtos, preços e condições de pagamento. O sistema permite a atualização automática de preços e notificação via SMS para clientes sempre que houver redução no preço de um produto que eles já adquiriram.

## Funcionalidades

- Cadastro de **clientes**, **produtos**, **preços** e **condições de pagamento**.
- Atualização de preços de produtos com **notificação automática** via SMS.
- Integração com a API do Twilio para envio de mensagens.
- Geração de relatórios em PDF com detalhes dos clientes e preços associados.

---

## Tecnologias Utilizadas

- **Python 3.12**
- **Django 5.1.5**
- **Django REST Framework**
- **xhtml2pdf** para geração de PDFs
- **Twilio API** para envio de SMS
- **PostgreSQL** (ou outro banco de dados suportado pelo Django)
- **python-dotenv** para gerenciamento de credenciais

---

## Instalação

### Requisitos Prévios

- Python 3.10+
- pip
- Banco de dados PostgreSQL (ou SQLite para desenvolvimento)

### Passo a Passo

1. Clone o repositório:

   ```bash
   https://github.com/MatrixRM/pagsys.git
   cd pagsys
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco de dados no arquivo `settings.py` ou crie um arquivo `.env` para armazenar as configurações sensíveis:

   ```env
   DATABASE_URL=postgres://usuario:senha@localhost:5432/pagsys
   TWILIO_ACCOUNT_SID=seu_account_sid
   TWILIO_AUTH_TOKEN=seu_auth_token
   TWILIO_PHONE_NUMBER=+seu_numero_twilio
   ```

5. Aplique as migrações:

   ```bash
   python manage.py migrate
   ```

6. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

---

## Uso

### 1. Acesse o Django Admin

- URL: http://127.0.0.1:8000/admin/
- Utilize as credenciais criadas com o comando:
  ```bash
  python manage.py createsuperuser
  ```

### 2. Teste o Envio de Notificações

- Altere o preço de um produto para um valor menor no Django Admin.
- Verifique os logs do servidor para mensagens de notificação enviadas.
- O cliente deve receber o SMS informando sobre a redução de preço.

---

## Estrutura do Projeto

```
pagsys/
├── api/
│   ├── models.py        # Modelos de dados
│   ├── serializers.py   # Serialização de dados para API
│   ├── views.py         # Lógica das views
│   ├── utils.py         # Funções auxiliares (Twilio e verificação de preços)
│   ├── signals.py       # Sinais para notificações automáticas
│   ├── templates/       # Templates HTML
│   └── urls.py          # Rotas do app
├── sistema_pagamentos/
│   ├── settings.py      # Configurações do Django
│   ├── urls.py          # Rotas principais
│   ├── wsgi.py          # Deploy
├── .env                 # Configurações sensíveis (não versionadas)
├── requirements.txt     # Dependências do projeto
└── manage.py            # Gerenciador do Django
```

---

## Contribuições

Contribuições são bem-vindas! Siga os passos abaixo para colaborar:

1. Faça um fork do repositório.
2. Crie uma branch com sua feature/bugfix:
   ```bash
   git checkout -b minha-branch
   ```
3. Commit suas alterações:
   ```bash
   git commit -m "Minha contribuição"
   ```
4. Faça um push para sua branch:
   ```bash
   git push origin minha-branch
   ```
5. Abra um Pull Request no repositório original.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## Contato

Em caso de dúvidas ou sugestões, entre em contato:

- **Email**: robertomanica@yahoo.com.br
- **LinkedIn**: https://www.linkedin.com/in/roberto-m%C3%A2nica-0876a21b7/
