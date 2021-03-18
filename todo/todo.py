from flask import (
    Blueprint, flash, g, url_for, redirect, request, render_template
)
from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__)

index_url = 'todo.index'

@bp.route('/')
@login_required
def index():
    db, c = get_db()
    user = g.user
    c.execute("""SELECT t.id, t.created_by, t.created_at, u.username, t.completed, t.description
                 FROM todo t JOIN "user" u ON t.created_by = u.id
                 WHERE u.id = %s 
                 ORDER BY t.created_at DESC""", (user['id'], ))
    todos = c.fetchall()
    print(todos)
    return render_template('todo/index.html', todos = todos)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
            error = 'La descripción no puede estar vacía'
        
        if error is not None:
            flash(error)
        else: 
            db, c = get_db()
            c.execute(""" 
                INSERT INTO todo(description, completed, created_by) 
                VALUES(%s, %s, %s) """, (description, False, g.user['id']))
            db.commit()
            return redirect(url_for(index_url))

    return render_template('todo/create.html')


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = get_todo(id, g.user['id'])
    if request.method == 'POST':
        description = request.form['description']
        completed = True if request.form.get('completed') == 'on' else False
        error = None

        if not description:
            error = 'La descripción no puede ser nula'
        
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(""" 
                UPDATE todo SET description = %s, completed = %s
                WHERE id = %s
            """, (description, completed, id))
            db.commit()
            return redirect(url_for(index_url))

    return render_template('todo/update.html', todo=todo)


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    todo = get_todo(id, g.user['id'])
    db, c = get_db()
    c.execute('DELETE FROM todo WHERE id = %s', (todo['id'], ))
    db.commit()
    return redirect(url_for(index_url))

def get_todo(id, user_id):
    db, c = get_db()
    c.execute("""SELECT t.*, u.username 
                 FROM todo t JOIN "user" u ON t.created_by = u.id 
                 WHERE t.id = %s 
                 AND   u.id = %s """, (id, user_id))
    todo = c.fetchone()
    if todo is None:
        abort('La tarea con ID {} no existe'.format(id))
    return todo
                