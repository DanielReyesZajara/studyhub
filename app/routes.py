from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from .extensions import db
from .models import Task
from .services import toggle_state, validate_description, validate_title

bp = Blueprint('tasks', __name__)


def find_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404)
    return task


def new_task(data):
    task = Task(title=validate_title(data.get('title')),
                description=validate_description(data.get('description', '')))
    db.session.add(task)
    db.session.commit()
    return task


@bp.get('/')
def index():
    tasks = db.session.scalars(db.select(Task).order_by(Task.id)).all()
    return render_template('index.html', tasks=tasks)


@bp.post('/tasks')
def create_task_form():
    try:
        new_task(request.form)
    except ValueError as error:
        return render_template('error.html', error=str(error)), 400
    return redirect(url_for('tasks.index'))


@bp.post('/tasks/<int:task_id>/toggle')
def toggle_task_form(task_id):
    task = find_task(task_id)
    task.completed = toggle_state(task.completed)
    db.session.commit()
    return redirect(url_for('tasks.index'))


@bp.post('/tasks/<int:task_id>/delete')
def delete_task_form(task_id):
    db.session.delete(find_task(task_id))
    db.session.commit()
    return redirect(url_for('tasks.index'))


@bp.get('/api/tasks')
def list_tasks():
    tasks = db.session.scalars(db.select(Task).order_by(Task.id)).all()
    return jsonify([task.to_dict() for task in tasks])


@bp.post('/api/tasks')
def create_task_api():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error='Se requiere un objeto JSON.'), 400
    try:
        task = new_task(data)
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(task.to_dict()), 201


@bp.post('/api/tasks/<int:task_id>/toggle')
def toggle_task_api(task_id):
    task = find_task(task_id)
    task.completed = toggle_state(task.completed)
    db.session.commit()
    return jsonify(task.to_dict())


@bp.delete('/api/tasks/<int:task_id>')
def delete_task_api(task_id):
    db.session.delete(find_task(task_id))
    db.session.commit()
    return '', 204


@bp.get('/health')
def health():
    try:
        db.session.execute(text('SELECT 1'))
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(status='error'), 503
    return jsonify(status='ok')
