from flask import Blueprint, abort, redirect, render_template, request
from app.services.task_service import TaskService

from datetime import datetime, timedelta

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def _parse_int_field(name, minimum=None, maximum=None):
    try:
        value = int(request.form[name])
    except (KeyError, TypeError, ValueError):
        abort(400)

    if minimum is not None and value < minimum:
        abort(400)
    if maximum is not None and value > maximum:
        abort(400)

    return value

def _normalize_scheduled_time(value):
    if not value:
        return (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M")

    try:
        return datetime.fromisoformat(value).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        abort(400)

def _scheduled_time_for_input(value):
    return value.replace(" ", "T") if value else ""

def _task_form_data():
    title = request.form.get("title", "").strip()
    if not title:
        abort(400)

    importance = _parse_int_field("importance", minimum=0, maximum=10)
    urgency = _parse_int_field("urgency", minimum=0, maximum=10)
    duration = _parse_int_field("duration", minimum=1)
    try:
        fixed = bool(int(request.form.get("fixed", 0)))
    except ValueError:
        abort(400)
    days = request.form.getlist("days_of_week")
    days_str = ",".join(days) if days else None
    scheduled_time = _normalize_scheduled_time(request.form.get("scheduled_time"))

    return {
        "title": title,
        "importance": importance,
        "urgency": urgency,
        "duration": duration,
        "scheduled_time": scheduled_time,
        "fixed": fixed,
        "days_of_week": days_str,
    }

@task_bp.route("/", methods=["GET", "POST"])
def list_tasks():

    if request.method == "POST":
        data = _task_form_data()
        TaskService.create_task(
            data["title"],
            data["importance"],
            data["urgency"],
            data["duration"],
            data["scheduled_time"],
            data["fixed"],
            data["days_of_week"],
        )

    return render_template("task/list.html", 
                           normal_tasks=TaskService.list_ordered_normal_tasks(), 
                           fixed_tasks=TaskService.list_fixed_tasks())

@task_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = TaskService.get_task(id)
    if not task:
        abort(404)

    if request.method == "POST":
        data = _task_form_data()
        task.update(data)
        
        task = TaskService.update_task(task)

    return render_template("task/edit.html", task=task, scheduled_time_value=_scheduled_time_for_input(task["scheduled_time"]))

@task_bp.route("/complete/<int:id>", methods=["POST"])
def complete(id):
    task = TaskService.get_task(id)
    if not task:
        abort(404)

    task['done'] = True
    TaskService.update_task(task)

    return redirect("/tasks/")

@task_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    task = TaskService.get_task(id)    
    if not task:
        abort(404)

    task['deleted'] = True
    TaskService.update_task(task)

    return redirect("/tasks/")
