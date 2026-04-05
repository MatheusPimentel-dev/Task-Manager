from app.services.task_service import TaskService
from datetime import datetime, timedelta
from app.services.telegram_service import TelegramService

def verificar_tarefas_pendentes():
    print("Rodando job...")

    task = TaskService.list_tasks_notification()
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M")

    for t in task:
        if t['scheduled_time'] == now and not t['done'] and not t['notification_sent']:
            message = f"📣 Tarefa: {t['title']} - Hora de realizar a tarefa! Duração: {t['duration']} minutos."

            if(t['fixed']):
                message = f"😁 Tarefa fixa: {t['title']} - Hora de realizar a tarefa! Duração: {t['duration']} minutos."
            elif(t['importance'] >= 9 or t['urgency'] >= 9):
                message = f"🔥 Tarefa Urgente: {t['title']} - Hora de realizar a tarefa! Duração: {t['duration']} minutos."

            TelegramService.send_message(message)

            t['notification_sent'] = True
            TaskService.update_task(t)