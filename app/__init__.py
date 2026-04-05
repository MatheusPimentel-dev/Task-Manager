from flask import Flask
from app.config import Config
from app.extensions import db, migrate

from app.scheduler.scheduler import start_scheduler

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar rotas
    from app.routes.task_routes import task_bp
    app.register_blueprint(task_bp)

    start_scheduler(app)

    return app