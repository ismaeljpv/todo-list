import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from werkzeug.security import check_password_hash, generate_password_hash
from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
login_url = 'auth.login'

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        print(username)
        c.execute('SELECT id FROM "user" WHERE username = %s', (username, ))
        
        if not username:
            error = 'Username es requerido'
        elif not password:
            error = 'Password es requerido'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado'.format(username)

        if error is None:
            c.execute(
                'INSERT INTO "user"(username, password) VALUES(%s, %s)',
                (username, generate_password_hash(password))
                )
            db.commit()
            return redirect(url_for(login_url))
        
        flash(error)
    
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None

        c.execute('SELECT * FROM "user" WHERE username = %s', (username, ))
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña inválido.'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña inválidos.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))
        
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    try:
        user_id = session['user_id']
    except KeyError:
        user_id = None

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute('SELECT * FROM "user" WHERE id = %s', (user_id, ))
        user = c.fetchone()
        g.user = user


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for(login_url))
           
        return view(**kwargs)
        
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for(login_url))
