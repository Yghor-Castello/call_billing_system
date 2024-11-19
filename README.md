# Call Billing System API

## Descrição

API REST desenvolvida com Django e Django REST Framework para gerenciamento de chamadas telefônicas e faturamento. A aplicação permite que os usuários insiram, visualizem e gerenciem registros detalhados de chamadas, além de calcular automaticamente o custo das chamadas com base na duração, horários tarifários e taxas aplicáveis. A autenticação é realizada via token JWT.

## Tecnologias Utilizadas

- **Django** e **Django REST Framework**
- **PostgreSQL** (via Docker)
- **Docker** e **Docker Compose**
- **Autenticação via Token JWT**

## Funcionalidades

- **Gerenciamento de Empréstimos**: Registro e visualização de chamadas telefônicas com dados como origem, destino, duração e horário.
- **Gerenciamento de Pagamentos**: Cálculo automático do custo das chamadas com base na duração, horários tarifários e taxas aplicáveis.
- **Autenticação JWT**: Garantia de que os usuários só podem acessar e gerenciar seus próprios registros e faturas de chamadas.
- **Soft Delete**: Registros não são deletados permanentemente, mas marcados como removidos para maior segurança e rastreabilidade.

## Instruções para Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/xxxxxxxxxxxxxxxxx
cd call-billiing-system-api
```

### 2. Configurar e Iniciar com Docker

```
docker-compose up --build
```

### 3. Aplicar Migrações e Criar Superusuário

```
docker-compose exec backend python manage.py migrate
```
```
docker-compose exec backend python manage.py createsuperuser
```

### 4. Carregamento das fixtures para popular o banco de dados

```
docker-compose exec backend python manage.py loaddata billing_fixture.json
```

### 5. Acessar a API

- A API estará disponível em http://localhost:8000/.

### 6. Executando Testes

```
docker-compose exec backend pytest
```

### 7. Insomnia Collection

- Para testar a API via Insomnia acesse a pasta insomnia_collection e import o arquivo json no seu Insomnia.# call_billing_system

<!-- Endpoint que precisamos passar para conferir as rotas.  -->
- http://localhost:8000/api/phone-bills?phone_number=99988526423&period=2016-02
- http://localhost:8000/api/phone-bills?phone_number=99988526423&period=2017-12
- http://localhost:8000/api/phone-bills?phone_number=99988526423
- http://localhost:8000/api/phone-bills?phone_number=99988526423&period=2015-01