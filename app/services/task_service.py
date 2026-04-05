from app.repositories.task_repository import TaskRepository
from datetime import datetime, timedelta

class TaskService:

    @staticmethod
    def get_task(id):
        task = TaskRepository.get_by_id(id)
        return task.to_dict() if task else None

    @staticmethod
    def list_tasks():
        tasks = TaskRepository.get_all()
        return [t.to_dict() for t in tasks]
    
    @staticmethod
    def list_tasks_notification():
        tasks = TaskService.list_ordered_normal_tasks()
        tasks.extend(TaskService.list_fixed_tasks())

        return tasks
    
    @staticmethod
    def list_fixed_tasks():
        tasks = TaskRepository.get_fixed_tasks()
        return [t.to_dict() for t in tasks]

    @staticmethod
    def list_normal_tasks():
        tasks = TaskRepository.get_normal_tasks()
        return [t.to_dict() for t in tasks]

    @staticmethod
    def create_task(title, importance, urgency, duration, scheduled_time, fixed, days_of_week):
        weight = TaskService._calculate_priority(importance, urgency)
        return TaskRepository.create(title, importance, urgency, duration, scheduled_time, fixed, days_of_week, weight).to_dict()
    
    @staticmethod
    def update_task(task):
        weight = TaskService._calculate_priority(task['importance'], task['urgency'])
        task['weight'] = weight
        return TaskRepository.update(task)

    @staticmethod
    def _calculate_priority(importance, urgency):
        return (importance * 2) + urgency
    
    @staticmethod
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
    
    @staticmethod
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
    
    @staticmethod
    def free_slots(fixed_tasks):
        now = datetime.now()
        end_day = now.replace(hour=23, minute=0)

        blocks = TaskService.get_fixed_blocks(fixed_tasks, now.weekday())
        free_slots = TaskService.find_free_slots(blocks, now, end_day)
        
        return free_slots

    @staticmethod
    def list_ordered_normal_tasks():
        tasks = TaskService.list_normal_tasks()
        fixed_tasks = TaskService.list_fixed_tasks()

        free_slots = TaskService.free_slots(fixed_tasks);
        tasks_sorted = sorted(tasks, key=lambda x: x['weight'], reverse=True)

        scheduled = []

        for task in tasks_sorted:
            duration = timedelta(minutes=task['duration'])

            for i, (start, end) in enumerate(free_slots):
                if (end - start) >= duration:                
                    task['scheduled_time'] = start.strftime("%Y-%m-%d %H:%M")

                    free_slots[i] = (start + duration, end)

                    scheduled.append(task)
                    break

        return scheduled