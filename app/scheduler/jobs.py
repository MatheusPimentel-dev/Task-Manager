from app.services.task_service import TaskService
from datetime import datetime, timedelta
from app.services.telegram_service import TelegramService

def verificar_tarefas_pendentes():
    print("Rodando job...")

    task = TaskService.list_tasks_notification()
    horarioAtual = datetime.now()
    now = horarioAtual.strftime("%Y-%m-%d %H:%M")

    for t in task:
        if horarioAtual.hour == 0 and horarioAtual.minute == 0:
            resetar_notificacoes(t)

        elif t['scheduled_time'] == now and not t['done'] and not t['notification_sent']:
            enviar_notificacao(t)


def resetar_notificacoes(task):
    task['notification_sent'] = False
    TaskService.update_task(task)


def enviar_notificacao(task):
    message = f"📣 Tarefa: {task['title']} - Hora de realizar a tarefa! Duração: {task['duration']} minutos."

    if(task['fixed']):
        message = f"😁 Tarefa fixa: {task['title']} - Hora de realizar a tarefa! Duração: {task['duration']} minutos."
    elif(task['importance'] >= 9 or task['urgency'] >= 9):
        message = f"🔥 Tarefa Urgente: {task['title']} - Hora de realizar a tarefa! Duração: {task['duration']} minutos."

    TelegramService.send_message(message)

    task['notification_sent'] = True
    TaskService.update_task(task)