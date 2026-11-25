from flask import Blueprint, request, session, redirect, url_for, render_template, flash, abort
from datetime import datetime
from decimal import Decimal
from database import database, TABLES

records_bp = Blueprint("records", __name__)

# Retrieve table column information
def columns(cur, table):
    cur.execute(
        'SELECT column_name, data_type, nullable '
        'FROM user_tab_columns '
        'WHERE table_name = :t '
        'ORDER BY column_id',
        t=table
    )
    return cur.fetchall()

# Convert input values into Oracle data types
def value(raw, kind):
    if raw == '':
        return None
    if kind == 'DATE':
        return datetime.fromisoformat(raw)
    if kind == 'NUMBER':
        return Decimal(raw)
    return raw

# Format database values
def display(v):
    if v is None:
        return ''
    if isinstance(v, datetime):
        return v.isoformat(sep='T', timespec='seconds')
    return str(v)

# View, insert, update and delete records
@records_bp.route('/table/<table>', methods=['GET', 'POST'])
def records(table):
    if table not in TABLES:
        abort(404)
    keys = TABLES[table]
    with database() as (conn, cur):
        meta = columns(cur, table)
        if not meta:
            return render_template('missing_table.html'), 404
        names = []
        kinds = {}
        for c in meta:
            names.append(c[0])
            kinds[c[0]] = c[1]
        if request.method == 'POST':
            action = request.form['action']
            vals = {}
            if action != 'delete':
                for c in names:
                    vals[c] = value(
                        request.form.get(c, ''),
                        kinds[c]
                    )
            # Insert record
            if action == 'insert':
                placeholders = []
                for c in names:
                    placeholders.append(':' + c)
                sql = (
                    f'INSERT INTO {table} '
                    f'({", ".join(names)}) '
                    f'VALUES ({", ".join(placeholders)})'
                )
                cur.execute(sql, vals)
            # Update or delete record
            elif action in ('update', 'delete'):
                binds = {}
                conditions = []
                for c in keys:
                    binds['old' + c] = value(
                        request.form['old' + c],
                        kinds[c]
                    )
                    conditions.append(c + '=:old' + c)
                where = ' AND '.join(conditions)
                if action == 'delete':
                    cur.execute(
                        f'DELETE FROM {table} WHERE {where}',
                        binds
                    )
                else:
                    updates = []
                    for c in names:
                        updates.append(c + '=:' + c)
                    sql = (
                        f'UPDATE {table} SET '
                        + ', '.join(updates)
                        + ' WHERE '
                        + where
                    )
                    vals.update(binds)
                    cur.execute(sql, vals)
                if cur.rowcount != 1:
                    raise ValueError('Record no longer exists.')
            else:
                abort(400)
            conn.commit()
            if action == 'delete':
                flash('Record deleted.')
            else:
                flash('Record saved.')
            return redirect(
                url_for('records.records', table=table)
            )
        # Search records
        search = request.args.get('q', '')
        sql = f'SELECT * FROM {table}'
        if search:
            conditions = []
            for c in names:
                if kinds[c] in ('NUMBER', 'DATE'):
                    conditions.append(
                        'INSTR(LOWER(TO_CHAR('
                        + c
                        + ')), LOWER(:q)) > 0'
                    )
                else:
                    conditions.append(
                        'INSTR(LOWER('
                        + c
                        + '), LOWER(:q)) > 0'
                    )
            sql += ' WHERE ' + ' OR '.join(conditions)
        sql += ' ORDER BY ' + ', '.join(keys)
        if search:
            cur.execute(sql, {'q': search})
        else:
            cur.execute(sql)
        rows = []
        for r in cur.fetchall():
            rows.append(dict(zip(names, map(display, r))))
    return render_template('records.html',
    table=table,
    keys=keys,
    meta=meta,
    names=names,
    rows=rows,
    search=search)
