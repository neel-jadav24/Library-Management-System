from flask import Flask, request, session, redirect, url_for, render_template, abort
import secrets

from database import TABLES, credentials
from login import login_bp
from tables import tables
from records import records_bp
from reports import reports_bp


# Initialize Flask
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


# Register website pages
app.register_blueprint(login_bp)
app.register_blueprint(tables)
app.register_blueprint(records_bp)
app.register_blueprint(reports_bp)


# Shared navigation for HTML templates
@app.context_processor
def navigation():
    if session.get("login_id") in credentials:
        return {"tables": TABLES}

    return {"tables": {}}


# Protect pages from unauthorized access
@app.before_request
def guard():
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(24)

    if request.method == "POST":
        if request.form.get("csrf") != session["csrf"]:
            abort(400)

    if request.endpoint not in ("login.login", "static"):
        if session.get("login_id") not in credentials:
            return redirect(url_for("login.login"))


# Display errors
@app.errorhandler(Exception)
def error(e):
    if hasattr(e, "code"):
        return str(e), e.code

    return render_template("error.html", message=str(e)), 500


# Dashboard
@app.get("/")
def home():
    return render_template(
        "dashboard.html",
        tables=TABLES,

        actions=[
            ("drop", "Drop tables"),
            ("create", "Create tables"),
            ("populate", "Populate tables")
        ],

        descriptions={
            "drop": "Delete project tables and views. Use a dedicated schema.",
            "create": "Create missing normalized tables and reporting views.",
            "populate": "Insert sample records and skip duplicate records."
        }
    )


# Start Flask application
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )