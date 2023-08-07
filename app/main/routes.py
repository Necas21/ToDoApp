from flask import render_template, flash, redirect, url_for, request
from app.main import bp
from flask_login import current_user, login_required
from app.main.forms import TaskForm
from app.models import Task
from app import db


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    return render_template("index.html", user=current_user, tasks=current_user.tasks)


@bp.route("/complete_tasks")
@login_required
def complete_tasks():
    return render_template(
        "complete_tasks.html", user=current_user, tasks=current_user.tasks
    )


@bp.route("/create_task", methods=["GET", "POST"])
@login_required
def create_task():
    form = TaskForm()
    print(form.due_date.data)
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            owner=current_user,
        )
        db.session.add(task)
        db.session.commit()
        flash("Task Created!")
        return redirect(url_for("main.index"))
    return render_template("create_task.html", form=form)


@bp.route("/delete_task")
@login_required
def delete_task():
    try:
        task_id = int(request.args.get("task_id"))
    except:
        flash("Invalid Task ID!")
        return redirect(url_for("main.index"))
    if not current_user.tasks.filter_by(id=task_id).first():
        flash("Unable To Delete Task!")
        return redirect(url_for("main.index"))
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Successfully Deleted Task!")
    return render_template("index.html", user=current_user, tasks=current_user.tasks)


@bp.route("/complete_task")
@login_required
def complete_task():
    try:
        task_id = int(request.args.get("task_id"))
    except:
        flash("Invalid Task ID!")
        return redirect(url_for("main.index"))
    if not current_user.tasks.filter_by(id=task_id).first():
        flash("Unable To Complete Task!")
        return redirect(url_for("main.index"))
    task = Task.query.get_or_404(task_id)
    task.status = "complete"
    db.session.commit()
    flash("Successfully Completed Task!")
    return render_template("index.html", user=current_user, tasks=current_user.tasks)
