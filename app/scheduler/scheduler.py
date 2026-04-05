from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def start_scheduler(app):

    def job():
        with app.app_context():
            from app.scheduler.jobs import verificar_tarefas_pendentes
            verificar_tarefas_pendentes()

    scheduler.add_job(job, trigger="interval", minutes=1)
    scheduler.start()

