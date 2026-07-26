from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from extensions import db, bcrypt
from models.user import User

auth = Blueprint("auth", __name__)


# -----------------------------
# Register
# -----------------------------
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful. Please Login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# -----------------------------
# Login
# -----------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):

            login_user(user)

            user.last_login = db.func.now()
            db.session.commit()

            return redirect(url_for("resume.resume_builder"))

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")


# -----------------------------
# Logout
# -----------------------------
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged Out Successfully.", "success")

    return redirect(url_for("auth.login"))