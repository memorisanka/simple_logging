from datetime import datetime
from flask import Blueprint, request, render_template, redirect, session, flash, url_for
from . import db
from .models import Users


login_blueprint = Blueprint("login", __name__)
logout_blueprint = Blueprint("logout", __name__)
dashboard_blueprint = Blueprint("dashboard", __name__)
register_blueprint = Blueprint("register", __name__)


@login_blueprint.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]
        found_user = Users.query.filter_by(name=nickname).first()

        if not found_user:
            flash("You have to register.", "warning")
        else:
            session.update({"nick": nickname, "password": password})
            flash("You've been successfully logged in.", "success")

    elif request.method == "GET" and "nick" not in session:
        return render_template("login.html")
    elif request.method == "GET" and "nick" in session:
        flash("Already logged in!", "warning")

    return redirect(url_for("dashboard.dashboard"))


@login_blueprint.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]
        password_repeat = request.form["password2"]
        registration_date = datetime.now()
        found_user = Users.query.filter_by(name=nickname).first()

        if not found_user and password == password_repeat:
            new_user = Users(name=nickname, registration_date=registration_date, password=password)
            db.session.add(new_user)
            db.session.commit()
            session.update({"nick": nickname, "password": password})

            flash("You've been successfully registered.", "success")
        elif found_user:
            flash("You've been already registered. Please, log in.", "warning")
            return redirect(url_for("login.login"))
        else:
            flash("Ups...something went wrong...", "warning")
            return render_template("register.html")

    elif request.method == "GET" and "nick" not in session:
        return render_template("register.html")
    elif request.method == "GET" and "nick" in session:
        flash("Already logged in!", "warning")

    return redirect(url_for("dashboard.dashboard"))


@logout_blueprint.route("/logout")
def logout():
    if "nick" in session:
        session.pop("nick", None)
        session.pop("email", None)
        flash("You have been logged out!", "success")
    else:
        flash("You are not logged in!", "warning")

    return redirect(url_for("login.login"))


@dashboard_blueprint.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    if "nick" in session:
        nickname = session["nick"]
        query = Users.query.filter_by(name=f"{nickname}").first()
        date_of_register = query.registration_date
        days_from_register = (datetime.date(datetime.now()) - date_of_register).days

        return render_template("dashboard.html", nickname=nickname, date=days_from_register)
    else:
        flash("You are not logged in!", "warning")

    return redirect(url_for("login.login"))
