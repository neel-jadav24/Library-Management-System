from flask import Blueprint, request, session, redirect, url_for, render_template, flash, abort
import json
from database import BASE, database

REPORTS = json.loads((BASE / "reports.json").read_text())

reports_bp = Blueprint("reports", __name__)

# Execute predefined SQL reports
@reports_bp.get('/reports')
def reports():
    selected = request.args.get('report')
    rows = []
    names = []
    if selected:
        if selected not in REPORTS:
            abort(404)
        with database() as (conn, cur):
            cur.execute(REPORTS[selected])
            for c in cur.description:
                names.append(c[0])
            rows = cur.fetchall()
    return render_template('reports.html',
    reports=REPORTS,
    selected=selected,
    sql=REPORTS.get(selected),
    rows=rows,
    names=names)
