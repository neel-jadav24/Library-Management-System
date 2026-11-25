from flask import Blueprint, request, session, redirect, url_for, render_template, flash
import secrets
import oracledb

from database import DSN, credentials

login_bp = Blueprint("login", __name__)


# Oracle login page
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"].strip()
        password = request.form["password"]

        try:
            with oracledb.connect(
                user=user,
                password=password,
                dsn=DSN
            ) as conn:

                with conn.cursor() as cur:
                    cur.execute("SELECT 1 FROM dual")
                    cur.fetchone()

        except oracledb.Error as e:
            flash("Oracle connection failed: " + str(e))

        else:
            credentials.pop(session.get("login_id"), None)

            session.clear()
            session["login_id"] = secrets.token_hex(32)

            credentials[session["login_id"]] = (user, password)

            return redirect(url_for("home"))

    return render_template("login.html")


# Log out
@login_bp.post("/exit")
def exit_app():
    credentials.pop(session.get("login_id"), None)

    session.clear()

    return redirect(url_for("login.login"))