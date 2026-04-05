from datetime import datetime, timedelta
from models import get_connection

def get_fixed_blocks(tasks, current_day):
    blocks = []

    for task in tasks:
        if task['days_of_week']:
            days = [int(d) for d in task['days_of_week'].split(",")]

            if current_day in days:
                start = datetime.strptime(task['scheduled_time'], "%Y-%m-%d %H:%M")
                end = start + timedelta(minutes=task['duration'])

                blocks.append((start, end))

    return blocks

def find_free_slots(blocks, start_day, end_day):
    free_slots = []
    current = start_day

    for block_start, block_end in sorted(blocks):
        if current < block_start:
            free_slots.append((current, block_start))
        current = max(current, block_end)

    if current < end_day:
        free_slots.append((current, end_day))

    return free_slots

def free_slots(fixed_tasks):
    now = datetime.now()
    end_day = now.replace(hour=23, minute=0)

    blocks = get_fixed_blocks(fixed_tasks, now.weekday())
    free_slots = find_free_slots(blocks, now, end_day)

    return free_slots

def calculoImportancia(importancia, urgencia):    
    return (importancia * 2) + urgencia

def obter_tarefas_normais():
    conn = get_connection() 
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM tasks 
        WHERE fixed = 0 AND done = 0
        ORDER BY weight DESC
        """)
    normal_tasks = cursor.fetchall()

    normal_tasks = [dict(t) for t in normal_tasks]
    return normal_tasks

def obter_tarefas_fixas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM tasks 
    WHERE fixed = 1
    ORDER BY scheduled_time ASC
    """)
    fixed_tasks = cursor.fetchall()
    fixed_tasks = [dict(t) for t in fixed_tasks]
    return fixed_tasks

def atualizar_horario_tarefa(id, novo_horario):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET scheduled_time = ?
    WHERE id = ?
    """, (novo_horario, id))

    conn.commit()
    conn.close()