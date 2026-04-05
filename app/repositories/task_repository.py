from app.models.task import Task
from app.extensions import db

class TaskRepository:

    @staticmethod
    def get_by_id(id):
        return Task.query.get(id)

    @staticmethod
    def get_all():
        return Task.query.filter_by(deleted=False).all()
    
    @staticmethod
    def get_fixed_tasks():
        return Task.query.filter_by(fixed=True, done=False, deleted=False).all()
    
    @staticmethod
    def get_normal_tasks():
        return Task.query.filter_by(fixed=False, done=False, deleted=False).all()

    @staticmethod
    def create(title, importance, urgency, duration, scheduled_time, fixed, days_of_week, weight):
        task = Task(title=title, importance=importance, urgency=urgency, duration=duration,
                    scheduled_time=scheduled_time, fixed=fixed, days_of_week=days_of_week, weight=weight)
        db.session.add(task)
        db.session.commit()
        return task
    
    @staticmethod
    def update(task):
        taskdb = Task.query.get(task['id'])
        if not taskdb:
            return None
        
        taskdb.update(task)
        db.session.commit()
        return task