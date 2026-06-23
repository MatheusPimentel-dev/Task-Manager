# Task Manager

Gerenciador pessoal de tarefas feito em **Python + Flask + SQLite**.

O objetivo do projeto é ajudar na organização diária de tarefas, priorizando o que deve ser feito primeiro com base em **importância**, **urgência**, duração estimada e horários já ocupados por tarefas fixas.

## Para Que Serve

O sistema permite:

- cadastrar tarefas comuns;
- cadastrar tarefas fixas/recorrentes por dia da semana;
- calcular prioridade automaticamente;
- montar uma lista sugerida de tarefas do dia;
- concluir tarefas;
- excluir tarefas sem apagar fisicamente do banco, usando soft delete;
- enviar notificações pelo Telegram quando uma tarefa chega no horário agendado.

É um MVP local, pensado para uso pessoal, mas com estrutura suficiente para crescer com novas funcionalidades.

## Como Funciona Para Usuários

A aplicação roda no navegador em:

```text
http://localhost:5003/tasks/
```

Na tela principal é possível criar uma nova tarefa informando:

- **Título**: nome da tarefa.
- **Importância**: de `0` a `10`.
- **Urgência**: de `0` a `10`.
- **Duração**: tempo estimado em minutos.
- **Horário**: opcional; se ficar vazio, o sistema agenda para 10 minutos após o cadastro.
- **Dias da semana**: usado para tarefas recorrentes.
- **Tarefa fixa**: marca a tarefa como parte da rotina fixa.

A prioridade é calculada com a fórmula:

```text
peso = (importância * 2) + urgência
```

Tarefas com maior peso aparecem primeiro na agenda sugerida.

## Stack Técnica

- Python
- Flask
- Jinja2
- SQLite
- SQLAlchemy
- Flask-Migrate / Alembic
- APScheduler
- Requests
- python-dotenv
- unittest

## Estrutura Do Projeto

```text
.
├── app/
│   ├── models/           # Modelos SQLAlchemy
│   ├── repositories/     # Acesso ao banco de dados
│   ├── routes/           # Rotas HTTP e blueprints Flask
│   ├── scheduler/        # Scheduler e jobs periódicos
│   ├── services/         # Regras de negócio
│   ├── templates/        # Templates HTML/Jinja2
│   ├── config.py         # Configurações da aplicação
│   ├── extensions.py     # Extensões Flask: db e migrate
│   └── __init__.py       # Application factory
├── instance/             # Banco SQLite local
├── migrations/           # Migrações Alembic
├── tests/                # Testes automatizados
├── run.py                # Ponto de entrada da aplicação
├── requirements.txt      # Dependências Python
├── .env-exemplo          # Exemplo de variáveis de ambiente
└── readme.md
```

## Requisitos

- Python 3.10 ou superior.
- Windows PowerShell, se estiver usando Windows.

O projeto já possui um ambiente virtual `venv` neste workspace. Em outra máquina, crie um novo ambiente virtual.

## Instalação

Crie e ative o ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r .\requirements.txt
```

Se o comando `python` apontar para o alias da Microsoft Store no Windows, use diretamente:

```powershell
.\venv\Scripts\python.exe
```

## Configuração Do Telegram

A integração com Telegram é opcional.

Crie um arquivo `.env` na raiz do projeto usando `.env-exemplo` como referência:

```env
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=
```

Campos:

- `TELEGRAM_TOKEN`: token do bot criado no Telegram.
- `TELEGRAM_CHAT_ID`: ID do chat que receberá as mensagens.

Se essas variáveis não estiverem preenchidas, o sistema simplesmente não envia notificações e continua funcionando.

## Banco De Dados

O projeto usa SQLite e grava o banco em:

```text
instance/database.db
```

Para aplicar as migrações existentes:

```powershell
.\venv\Scripts\flask.exe db upgrade
```

Se estiver criando o projeto do zero em outro ambiente, defina a aplicação Flask antes de rodar comandos do Flask:

```powershell
$env:FLASK_APP = "run.py"
.\venv\Scripts\flask.exe db upgrade
```

Use `flask db init` apenas se a pasta `migrations/` não existir. Neste projeto ela já existe.

## Como Rodar

Com o ambiente virtual ativo:

```powershell
python .\run.py
```

Ou usando o Python do `venv` diretamente:

```powershell
.\venv\Scripts\python.exe .\run.py
```

A aplicação sobe em:

```text
http://localhost:5003/tasks/
```

O `run.py` usa:

```python
app.run(debug=False, host="0.0.0.0", port=5003, use_reloader=False)
```

## Scheduler E Notificações

O scheduler roda em background usando APScheduler.

Ele executa o job de verificação a cada 1 minuto:

```text
verificar_tarefas_pendentes
```

Esse job:

- lista tarefas normais ordenadas por prioridade;
- lista tarefas fixas;
- verifica se alguma tarefa está agendada para o minuto atual;
- envia notificação pelo Telegram quando configurado;
- marca `notification_sent=True` após envio.

O scheduler foi configurado para evitar múltiplos registros do mesmo job quando a aplicação é criada mais de uma vez.

## Rotas Principais

```text
GET  /tasks/              Lista tarefas e exibe formulário de criação
POST /tasks/              Cria tarefa
GET  /tasks/edit/<id>     Exibe formulário de edição
POST /tasks/edit/<id>     Atualiza tarefa
POST /tasks/complete/<id> Marca tarefa como concluída
POST /tasks/delete/<id>   Marca tarefa como excluída
```

As ações de concluir e excluir usam `POST` para evitar alterações acidentais por navegação, refresh, crawler ou preview de link.

## Regras De Validação

Ao criar ou editar tarefas:

- `title` é obrigatório.
- `importance` deve estar entre `0` e `10`.
- `urgency` deve estar entre `0` e `10`.
- `duration` deve ser maior ou igual a `1`.
- `scheduled_time` deve ser uma data válida no formato aceito por `datetime-local`.

Se `scheduled_time` não for informado, o sistema define automaticamente:

```text
agora + 10 minutos
```

Internamente, o horário ainda é salvo como string no formato:

```text
YYYY-MM-DD HH:MM
```

Essa decisão foi mantida para evitar uma migração maior neste momento.

## Como Rodar Os Testes

O projeto usa `unittest`, biblioteca padrão do Python.

Execute:

```powershell
.\venv\Scripts\python.exe -m unittest discover -v
```

Resultado esperado:

```text
Ran 14 tests
OK
```

Os testes ficam em:

```text
tests/
```

Cobertura atual:

- cálculo de prioridade;
- ordenação de tarefas normais por peso;
- cálculo de blocos fixos;
- cálculo de horários livres;
- comportamento quando uma tarefa não cabe em nenhum horário livre;
- criação de tarefa via rota;
- rejeição de dados inválidos;
- edição de tarefa;
- conclusão via `POST`;
- exclusão via `POST`;
- garantia de que `GET` não conclui nem exclui tarefa;
- envio Telegram mockado;
- comportamento do Telegram sem configuração;
- falha controlada em erro de rede.

## Guia Para Desenvolvedores

### Onde Colocar Cada Tipo De Código

- **Modelos**: `app/models/`
  - Definem tabelas e campos do banco.

- **Repositórios**: `app/repositories/`
  - Fazem queries e persistência.
  - Devem evitar regras de negócio.

- **Serviços**: `app/services/`
  - Contêm regras de negócio.
  - Exemplo: priorização, cálculo de horários livres, integração Telegram.

- **Rotas**: `app/routes/`
  - Recebem requests HTTP.
  - Validam entrada.
  - Chamam serviços.
  - Renderizam templates ou redirecionam.

- **Templates**: `app/templates/`
  - HTML com Jinja2.
  - Devem evitar regra de negócio complexa.

- **Scheduler**: `app/scheduler/`
  - Jobs periódicos e inicialização do APScheduler.

### Fluxo De Uma Tarefa

1. Usuário envia formulário em `/tasks/`.
2. A rota valida os dados.
3. `TaskService.create_task()` calcula o peso.
4. `TaskRepository.create()` salva no banco.
5. A listagem chama `TaskService.list_ordered_normal_tasks()`.
6. O serviço calcula horários livres considerando tarefas fixas.
7. A tela exibe tarefas normais e rotina fixa.

### Como Criar Uma Nova Funcionalidade

Antes de implementar:

1. Verifique se a mudança é regra de negócio, rota, modelo ou UI.
2. Adicione ou ajuste testes primeiro quando possível.
3. Mantenha validação de entrada nas rotas.
4. Mantenha regra de negócio nos serviços.
5. Mantenha acesso ao banco nos repositórios.
6. Rode a suíte completa de testes.

Exemplo: adicionar categoria em tarefas.

1. Criar campo no model `Task`.
2. Gerar migration com Flask-Migrate.
3. Atualizar repository para persistir o campo.
4. Atualizar service se houver regra de categoria.
5. Atualizar formulário/listagem.
6. Adicionar testes de criação, edição e listagem.

## Migrações

Quando alterar modelos:

```powershell
$env:FLASK_APP = "run.py"
.\venv\Scripts\flask.exe db migrate -m "descricao da mudanca"
.\venv\Scripts\flask.exe db upgrade
```

Sempre revise o arquivo gerado em `migrations/versions/` antes de aplicar em ambientes importantes.

## Convenções Do Projeto

- Não colocar regra de negócio pesada em templates.
- Não acessar `request.form` dentro de services.
- Não fazer queries SQLAlchemy diretamente em rotas quando já existir repository.
- Preferir `POST` para ações que alteram dados.
- Manter testes para mudanças em regras de agenda, prioridade e recorrência.
- Não versionar `.env`.
- Evitar iniciar scheduler em testes.

## Limitações Conhecidas

- Não há autenticação, pois o uso atual é local/pessoal.
- `scheduled_time` ainda é salvo como string.
- Recorrência semanal é simples e baseada em `days_of_week`.
- Não há tela de histórico de tarefas concluídas ou excluídas.
- Não há tratamento visual amigável para todos os erros de validação; erros inválidos podem retornar `400`.

## Próximas Melhorias Sugeridas

- Migrar `scheduled_time` para `DateTime`.
- Criar tela para tarefas concluídas.
- Criar tela para tarefas excluídas/arquivadas.
- Melhorar mensagens de validação na interface.
- Adicionar categorias ou projetos.
- Adicionar filtros por prioridade, status e data.
- Criar configuração de horário útil por usuário.
- Melhorar recorrência para tarefas diárias, semanais e mensais.

