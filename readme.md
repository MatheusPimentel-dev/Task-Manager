# Task Manager (MVP local)

Gerenciador de tarefas local feito em **Flask + SQLite**, com:
- CRUD de tarefas (listar, criar, editar, concluir e “excluir” via soft delete)
- Priorização por **importância** e **urgência**
- Rotina fixa (tarefas recorrentes por dia da semana)
- Scheduler que verifica tarefas a cada minuto e pode enviar notificação via **Telegram**

## Stack
- Python + Flask (templates Jinja2)
- SQLite + SQLAlchemy + Flask-Migrate (Alembic)
- APScheduler (jobs em background)
- Requests (integração com Telegram)

## Estrutura do projeto

```
.
├─ app/
│  ├─ models/           # Modelos SQLAlchemy
│  ├─ repositories/     # Acesso ao banco (queries/CRUD)
│  ├─ routes/           # Blueprints/rotas HTTP
│  ├─ scheduler/        # Scheduler e jobs periódicos
│  ├─ services/         # Regras de negócio
│  ├─ templates/        # HTML (Jinja2)
│  ├─ config.py         # Configurações (ex.: DB)
│  ├─ extensions.py     # db/migrate
│  └─ __init__.py       # create_app + rotas + scheduler
├─ instance/            # Banco local (SQLite) e dados de runtime
├─ migrations/          # Migrações Alembic
├─ run.py               # Entry-point (Flask app)
├─ requirements.txt
├─ .env                 # Variáveis de ambiente (não versionar)
└─ .env-exemplo
```

## Requisitos
- Python 3.10+ (recomendado)

## Instalação

1) (Opcional) criar e ativar ambiente virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2) Instalar dependências

```powershell
pip install -r .\requirements.txt
```

## Configuração do Telegram (opcional)

Crie um arquivo `.env` na raiz (use `.env-exemplo` como base):

```env
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=
```

- `TELEGRAM_TOKEN`: token do bot
- `TELEGRAM_CHAT_ID`: id do chat onde o bot envia a notificação

## Banco de dados (migrações)

O projeto usa SQLite e cria o arquivo em `instance/database.db`.

```powershell
flask db init
flask db migrate -m "init"
flask db upgrade
```

Observação: `flask db init` só é necessário na primeira vez (quando não existe a pasta `migrations/`).

## Como rodar

```powershell
python .\run.py
```

A aplicação registra o blueprint em `/tasks`.

## Notificações (scheduler)

O scheduler roda em background e executa um job a cada 1 minuto para verificar tarefas pendentes e, se configurado, enviar mensagem no Telegram.

## Roadmap (ideias rápidas)
- Persistir `scheduled_time` como `DateTime` (evitar comparação de string)
- Melhorar regra de agendamento (janelas e conflitos)
- Melhorar UX (datas/horários, recorrência, filtros e histórico)
