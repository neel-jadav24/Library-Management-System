from flask import Blueprint, request, session, redirect, url_for, render_template, flash, abort
import oracledb
from database import database, script, TABLES

tables = Blueprint("tables", __name__)

# Create, drop and populate tables
@tables.post('/admin/<action>')
def admin(action):
    if action not in ('drop', 'create', 'populate'):
        abort(404)
    with database() as (conn, cur):
        if action == 'drop':
            if request.form.get('confirm') != 'on':
                abort(400)
            objects = [
                ('AVAILABLE_BOOKS', 'VIEW'),
                ('OUTSTANDING_FINES', 'VIEW'),
                ('BORROWED_BOOKS', 'VIEW')
            ]
            for t in reversed(TABLES):
                objects.append((t, 'TABLE'))
            for name, kind in objects:
                try:
                    cur.execute(f'DROP {kind} {name}')
                except oracledb.DatabaseError as e:
                    if e.args[0].code != 942:
                        raise
        elif action == 'create':
            # Create only missing tables
            script(cur, 'create')
            # Create or replace reporting views
            script(cur, 'views')
        else:
            script(cur, 'populate')
        conn.commit()
    flash(action.title() + ' completed.')
    return redirect('/')
