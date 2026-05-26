# SIGE UFPI — Sistema CRUD de Equipamentos de Informática

Sistema web fullstack para gerenciamento de equipamentos de informática da **Universidade Federal do Piauí (UFPI)**.
Ele permite autenticação via **JWT**, cadastro/consulta/edição/exclusão (soft delete) de equipamentos e um **dashboard administrativo** com estatísticas por status e localização.

## Tecnologias Utilizadas

- Backend: **Python**, **Flask**, **Flask-SQLAlchemy**, **Flask-JWT-Extended**, **Flask-Bcrypt**, **Flask-CORS**
- Banco de dados: **MySQL**
- Frontend: **HTML + CSS + JavaScript puro** com **Axios**

## Estrutura do Projeto

```text
sige/
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── middlewares/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── config.py
│   ├── run.py
│   ├── seed.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── pages/
│   ├── css/
│   ├── services/
│   ├── layouts/
│   ├── scripts/
│   └── components/
└── README.md
```

## Regras de Negócio (Implementadas)

- **RN01:** Número de patrimônio deve ser único (considerando somente registros não descartados).
- **RN02:** Equipamentos com status **descartado** não podem ser editados.
- **RN03:** Apenas **administradores** podem excluir equipamentos (exclusão lógica/soft delete por padrão).
- **RN04:** Campos obrigatórios: `patrimonio`, `nome`, `tipo`, `status`, `localizacao`.

## Como Instalar

### 1) Pré-requisitos

- Python 3.10+
- MySQL 8+
- Navegador moderno

### 2) Configurar o Banco MySQL

No MySQL, crie o banco:

```sql
CREATE DATABASE sige_ufpi
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

### 3) Criar o Ambiente Virtual

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
```

### 4) Instalar Dependências

```powershell
pip install -r requirements.txt
```

### 5) Configurar `.env`

Copie e edite:

```powershell
copy .env.example .env
```

Edite o arquivo `backend/.env` com suas credenciais:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=SUA_SENHA
DB_NAME=sige_ufpi
```

## Como Executar o Backend

```powershell
cd backend
.\venv\Scripts\activate
python run.py
```

A API estará disponível em:
- `http://localhost:5000/api/health`

## Como Executar o Frontend

O frontend fica em `frontend/` (HTML + CSS + JavaScript puro).

1. Abra a pasta `frontend` em um servidor HTTP (evite abrir com `file://`).

Exemplo com Python:

```powershell
cd frontend
python -m http.server 5500
```

2. Acesse:
- `http://localhost:5500`

## Como Rodar Seed Inicial

O seed cria as tabelas e insere usuários e equipamentos de exemplo quando o banco estiver vazio:

```powershell
cd backend
.\venv\Scripts\activate
python seed.py
```

## Usuários de Teste (Seed)

| E-mail | Senha | Perfil |
|---|---|---|
| admin@ufpi.edu.br | admin123 | Administrador |
| tecnico@ufpi.edu.br | tecnico123 | Técnico |
| visitante@ufpi.edu.br | visitante123 | Visitante |

## Rotas da API

Base: `http://localhost:5000/api`

### Autenticação

| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/login` | Login com `email` e `password` (retorna JWT) |

### Equipamentos

| Método | Rota | Permissão |
|---|---|---|
| GET | `/equipments` | Autenticado (busca, filtros e paginação) |
| GET | `/equipments/<id>` | Autenticado |
| POST | `/equipments` | Administrador e Técnico |
| PUT | `/equipments/<id>` | Administrador e Técnico |
| DELETE | `/equipments/<id>` | Administrador (soft delete por padrão) |

Parâmetros de listagem:
- `page`, `per_page`
- `search` (busca em tempo real por múltiplos campos)
- `status`, `tipo`, `localizacao`

Exclusão física (opcional):
- `DELETE /equipments/<id>?hard=true`

### Dashboard

| Método | Rota | Descrição |
|---|---|---|
| GET | `/dashboard/stats` | Estatísticas e agregações (status e localização) — Admin |

### Usuários (Admin)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/users` | Lista com paginação e busca |
| GET | `/users/<id>` | Recupera usuário |
| POST | `/users` | Cria usuário |
| PUT | `/users/<id>` | Atualiza usuário |
| DELETE | `/users/<id>` | Remove usuário |

## Como Gerar JWT

1. Envie requisição para o endpoint de login:

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"admin@ufpi.edu.br\",\"password\":\"admin123\"}"
```

2. No retorno, use o `token` para chamar as rotas protegidas:

`Authorization: Bearer <token>`

## Telas (prints/descrição)

Sem prints anexados aqui, mas a aplicação oferece:

- **Login:** card central com identidade visual UFPI.
- **Dashboard:** cards com total e quantidades por status + tabelas por status e setor (localização).
- **Equipamentos:** tabela paginada com busca em tempo real e filtros (status, tipo, localização) e modal para formulário (novo/editar/visualizar).

## Licença do Projeto

MIT License (projeto acadêmico).

