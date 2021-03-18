import psycopg2
import psycopg2.extras
import click
from flask import current_app, g
from flask.cli import with_appcontext
from todo.schema import instructions

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
                host=current_app.config['DATABASE_HOST'],
                database=current_app.config['DATABASE'],
                user=current_app.config['DATABASE_USER'],
                password=current_app.config['DATABASE_PASSWORD']
                )
        g.c = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db, c = get_db()
    for i in instructions:
        c.execute(i)
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)