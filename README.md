# Hubbi Auto API

> Desafio Técnico Backend desenvolvido para a Hubbi.

API REST construída com Django REST Framework para gerenciamento de um marketplace de autopeças. O projeto inclui importação assíncrona de catálogos via CSV, autenticação JWT, consultor de IA com Gemini e integração externa por API Key.

---

## Tecnologias utilizadas

- Python 3.12
- Django 5
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- Docker
- Docker Compose
- JWT (SimpleJWT)
- Gemini API
- drf-spectacular (Swagger/OpenAPI)
- Pytest

---

## Funcionalidades

### Marketplace

- Listagem de produtos
- Detalhes do produto
- Cadastro de produtos (Admin)
- Atualização de produtos (Admin)
- Exclusão de produtos (Admin)

### Importação Assíncrona

- Upload de arquivos CSV
- Processamento via Celery
- Persistência automática no PostgreSQL

### Consultor IA

- Consulta em linguagem natural via Gemini
- Resposta baseada no contexto dos produtos cadastrados

### Integração Externa

- Atualização de estoque em lote via API Key
- Não exige autenticação JWT

### Segurança

- Autenticação JWT
- API Key para integrações externas
- Permissões diferenciadas para usuários comuns e administradores

---

## Estrutura do projeto

```
apps/
├── common/
├── consultant/
├── integrations/
├── products/
└── users/
config/
media/
docker-compose.yml
Dockerfile
requirements.txt
README.md
```

---

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo:

```env
SECRET_KEY=your-secret-key
DEBUG=True
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=your_host
POSTGRES_PORT=your_port
REDIS_URL=redis://localhost:6379/0
API_KEY=your_api_key
GEMINI_API_KEY=your_gemini_api_key
```

> Nota: o campo `JWT_SECRET` não é necessário se você estiver usando `SIMPLE_JWT` com as variáveis padrão.

---

## Executando com Docker

Subir todos os serviços:

```bash
docker compose up --build
```

Subir em segundo plano:

```bash
docker compose up -d
```

Parar containers:

```bash
docker compose down
```

Remover volumes:

```bash
docker compose down -v
```

---

##  Serviços disponíveis

| Serviço      | Porta |
|-------------|-------|
| Django      | 8000  |
| PostgreSQL  | 5432  |
| Redis       | 6379  |

---

## Aplicando migrações

```bash
docker compose exec web python manage.py migrate
```

---

## Criando administrador

```bash
docker compose exec web python manage.py createsuperuser
```

---

## Rodando o Celery

Se estiver rodando localmente fora do Docker:

```bash
celery -A config worker -l info
```

No Docker, o worker deve subir automaticamente pelo `docker-compose`.

---

## Documentação da API

- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

---

## Autenticação JWT

Obter token:

```http
POST /api/token/
```

Atualizar token:

```http
POST /api/token/refresh/
```

Usar no header:

```http
Authorization: Bearer <TOKEN>
```

---

## Endpoints principais

### Produtos

```http
GET /api/products/
POST /api/products/
PUT /api/products/{id}/
DELETE /api/products/{id}/
```

### Importação CSV

```http
POST /api/products/import/
```

Formato esperado do CSV:

```csv
nome,descricao,preco,quantidade_inicial
```

A importação é processada de forma assíncrona via Celery.

### Consultor IA

```http
POST /api/consultor/consult/
```

Exemplo de payload:

```json
{
  "message": "Meu carro está fazendo barulho na roda"
}
```

### Integração Externa

```http
POST /api/integrations/update-stock/
```

Header obrigatório:

```http
X-API-Key: <sua_api_key>
```

Payload de exemplo:

```json
[
  {"id": 1, "quantity": 30},
  {"id": 2, "quantity": 15}
]
```

---

## Executando os testes

Rodar todos os testes:

```bash
pytest
```

Modo verboso:

```bash
pytest -v
```

Mostrar prints de debug:

```bash
pytest -v -s
```

---

## Cobertura de testes

### Produtos

- Listagem
- Busca por ID
- Cadastro
- Atualização
- Remoção

### Importação CSV

- Importação válida
- Arquivo vazio
- Cabeçalho inválido
- Delimitador `;`
- Valor numérico inválido

### Celery

- Task de importação usando mock

### Consultor IA

- Mock da Gemini API

### Integração Externa

- API Key válida
- API Key inválida
- Produto inexistente
- Atualização em lote

---

## Diferenciais do projeto

- Arquitetura organizada em apps Django
- Separação clara entre ViewSets, Services e Clients
- Processamento assíncrono com Celery
- Integração com Gemini para IA
- API documentada via Swagger
- Containerização com Docker
- Autenticação JWT e API Key
- Testes automatizados com Pytest
- Tipagem com Type Hints
- Docstrings e código limpo seguindo boas práticas Django

Upload assíncrono utilizando Celery
Integração com Gemini
Swagger documentado
Docker
JWT
API Key
Testes automatizados com Pytest
Tipagem (Type Hints)
Docstrings
Código organizado seguindo boas práticas do Django