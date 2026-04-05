from flask import Flask, render_template, request, redirect
from models import create_table, get_connection
from scheduler import start_scheduler, schedule_tasks
from datetime import datetime

import utils

app = Flask(__name__)

create_table()
start_scheduler()


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_connection()    
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        importance = int(request.form["importance"])
        urgency = int(request.form["urgency"])
        duration = int(request.form["duration"])

        weight = utils.calculoImportancia(importance, urgency)

        scheduled_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        fixed = int(request.form.get("fixed", 0))
        days = request.form.getlist("days_of_week")
        days_str = ",".join(days) if days else None

        cursor.execute("""
        INSERT INTO tasks (title, importance, urgency, duration, weight, scheduled_time, fixed, days_of_week)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, importance, urgency, duration, weight, scheduled_time, fixed, days_str))

        conn.commit()
        return redirect("/")

    conn.close()

    tarefas_normais = utils.obter_tarefas_normais()
    tarefas_fixas = utils.obter_tarefas_fixas()        
    
    scheduled_tasks = schedule_tasks(tarefas_normais, tarefas_fixas)

    return render_template("index.html", normal_tasks=scheduled_tasks, fixed_tasks=tarefas_fixas)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]

        cursor.execute("""
        UPDATE tasks SET title = ?
        WHERE id = ?
        """, (title, id))

        conn.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    task = cursor.fetchone()

    return render_template("edit.html", task=task)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()

    return redirect("/")

@app.route("/complete/<int:id>")
def complete(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET done = 1 WHERE id = ?", (id,))
    conn.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)