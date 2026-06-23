from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
JOB_ID = "verificar_tarefas_pendentes"

def start_scheduler(app):

    def job():
        with app.app_context():
            from app.scheduler.jobs import verificar_tarefas_pendentes
            verificar_tarefas_pendentes()

    scheduler.add_job(job, trigger="interval", minutes=1, id=JOB_ID, replace_existing=True)

    if not scheduler.running:
        scheduler.start()

