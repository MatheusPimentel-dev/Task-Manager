from app.extensions import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    done = db.Column(db.Boolean, default=False)
    importance = db.Column(db.Integer, default=1)
    urgency = db.Column(db.Integer, default=1)
    duration = db.Column(db.Integer, default=30)  # Duration in minutes
    weight = db.Column(db.Integer, default=1)
    scheduled_time = db.Column(db.String(120), nullable=True)  # Store as string for simplicity
    fixed = db.Column(db.Boolean, default=False)
    days_of_week = db.Column(db.String(120), nullable=True)  # Store as
    notification_sent = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "importance": self.importance,
            "urgency": self.urgency,
            "duration": self.duration,
            "weight": self.weight,
            "scheduled_time": self.scheduled_time,
            "fixed": self.fixed,
            "days_of_week": self.days_of_week,
            "notification_sent": self.notification_sent,
            "deleted": self.deleted
        }
    
    def update(self, data):
        self.title = data.get("title", self.title)
        self.done = data.get("done", self.done)
        self.importance = data.get("importance", self.importance)
        self.urgency = data.get("urgency", self.urgency)
        self.duration = data.get("duration", self.duration)
        self.weight = data.get("weight", self.weight)
        self.scheduled_time = data.get("scheduled_time", self.scheduled_time)
        self.fixed = data.get("fixed", self.fixed)
        self.days_of_week = data.get("days_of_week", self.days_of_week)
        self.notification_sent = data.get("notification_sent", self.notification_sent)
        self.deleted = data.get("deleted", self.deleted)