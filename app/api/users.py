from app.api import bp
from flask import jsonify, url_for, request, abort
from app.models import User, Task
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth
from datetime import datetime


@bp.route("/user/<int:id>", methods=["GET"])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route("user/<int:id>/tasks", methods=["GET"])
@token_auth.login_required
def get_tasks(id):
    user = User.query.get_or_404(id)
    tasks = {}
    index = 0
    for task in user.tasks:
        tasks[index] = task.to_dict()
        index += 1
    return jsonify(tasks)


@bp.route("/user/create", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    if "username" not in data or "email" not in data or "password" not in data:
        return bad_request("Must include username, email and password fields")
    if User.query.filter_by(username=data["username"]).first():
        return bad_request("User already exists. Please choose another username.")
    if User.query.filter_by(email=data["email"]).first():
        return bad_request(
            "Email already exists. Please choose a different email address"
        )
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_user", id=user.id)
    return response


@bp.route("/task/create", methods=["POST"])
@token_auth.login_required
def create_task():
    user_id = token_auth.current_user().id
    data = request.get_json() or {}
    if "title" not in data:
        return bad_request("Must include a title field.")
    if "description" not in data:
        return bad_request("Must include a description field.")
    if "due_date" not in data:
        return bad_request("Must include a due_date field.")
    if not bool(datetime.strptime(data["due_date"], "%Y-%m-%d")):
        return bad_request("The field due_date must be in YYYY-MM-DD format.")
    due_date = f'{data["due_date"]} 00:00:00'
    data["due_date"] = due_date
    task = Task()
    task.from_dict(data)
    task.user_id = user_id
    db.session.add(task)
    db.session.commit()
    response = jsonify(task.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user_id)
    return response

@bp.route("/task/<int:id>/delete", methods=["GET"])
@token_auth.login_required
def delete_task(id):
    user_id = token_auth.current_user().id
    task = Task.query.filter_by(id=id).first_or_404()
    if user_id != task.user_id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    response = jsonify(task.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user_id)
    return response