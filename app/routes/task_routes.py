from flask import Blueprint, request, redirect, render_template, request
from app.services.task_service import TaskService

from datetime import datetime, timedelta

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("/", methods=["GET", "POST"])
def list_tasks():

    if request.method == "POST":
        title = request.form["title"]
        importance = int(request.form["importance"])
        urgency = int(request.form["urgency"])
        duration = int(request.form["duration"])
        fixed = int(request.form.get("fixed", 0))
        days = request.form.getlist("days_of_week")
        days_str = ",".join(days) if days else None

        scheduled_time = datetime.now() + timedelta(minutes=10)
        scheduled_time = scheduled_time.strftime("%Y-%m-%d %H:%M")
        
        task = TaskService.create_task(title, importance, urgency, duration, scheduled_time, fixed, days_str)

    return render_template("task/list.html", 
                           normal_tasks=TaskService.list_ordered_normal_tasks(), 
                           fixed_tasks=TaskService.list_fixed_tasks())

@task_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = TaskService.get_task(id)
    if request.method == "POST":
        title = request.form["title"]
        importance = int(request.form["importance"])
        urgency = int(request.form["urgency"])
        duration = int(request.form["duration"])

        task['title'] = title
        task['importance'] = importance
        task['urgency'] = urgency
        task['duration'] = duration
        
        task = TaskService.update_task(task)

    return render_template("task/edit.html", task=task)

@task_bp.route("/complete/<int:id>")
def complete(id):
    task = TaskService.get_task(id)
    if task:
        task['done'] = True
        TaskService.update_task(task)

    return redirect("/tasks/")

@task_bp.route("/delete/<int:id>")
def delete(id):
    task = TaskService.get_task(id)    
    if task:
        task['deleted'] = True
        TaskService.update_task(task)
        print("Deleting task:", task)

    return redirect("/tasks/")