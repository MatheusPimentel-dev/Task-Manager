meu_projeto/
│
├── app/
│   ├── __init__.py          # Criação da app Flask
│   ├── config.py            # Configurações
│   │
│   ├── extensions.py        # Instâncias (db, migrate, etc)
│   │
│   ├── models/              # Modelos (ORM)
│   │   └── task.py
│   │
│   ├── services/            # Regras de negócio
│   │   └── task_service.py
│   │
│   ├── routes/              # Rotas (controllers)
│   │   └── task_routes.py
│   │
│   ├── repositories/        # Acesso ao banco (opcional, mas top)
│   │   └── task_repository.py
│   │
│   ├── utils/               # Funções auxiliares
│   │
│   └── templates/           # HTML (se usar render_template)
│
├── instance/
│   └── database.db          # SQLite fica aqui (fora do código)
│
├── migrations/              # Alembic (se usar Flask-Migrate)
│
├── tests/
│
├── run.py                   # Ponto de entrada
├── requirements.txt
└── README.md