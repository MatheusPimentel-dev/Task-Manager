from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from telegram_service import send_message
import sqlite3

import utils

def check_tasks():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    now += timedelta(minutes=1)

    cursor.execute("""
    SELECT title FROM tasks
    WHERE scheduled_time = ? AND done = 0
    """, (now,))

    tasks = cursor.fetchall()

    for task in tasks:
        send_message(f"Hora de fazer: {task[0]}")

    conn.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_tasks, 'interval', minutes=1)
    scheduler.start()

def schedule_tasks(tasks, fixed_tasks):
    free_slots = utils.free_slots(fixed_tasks);
    tasks_sorted = sorted(tasks, key=lambda x: x['weight'], reverse=True)

    scheduled = []

    for task in tasks_sorted:
        duration = timedelta(minutes=task['duration'])

        for i, (start, end) in enumerate(free_slots):
            if (end - start) >= duration:                
                task['scheduled_time'] = start.strftime("%Y-%m-%d %H:%M")
                utils.atualizar_horario_tarefa(task['id'], task['scheduled_time']);

                free_slots[i] = (start + duration, end)

                scheduled.append(task)
                break

    return scheduled

