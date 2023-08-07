from flask import render_template, url_for, redirect, flash, request, current_app
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm, PasswordResetForm, PasswordChangeForm
from app.models import User
from app import db
from app.auth.email import send_password_reset_email


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            current_app.logger.info(f"Failed login by user {form.username.data} from {request.remote_addr}")
            flash("Invalid username or password")
            return redirect("auth.login")
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        current_app.logger.info(f"Successfull login by user {user.username} from {request.remote_addr}")
        return redirect(next_page)
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash("Username already exists!")
            return redirect(url_for("auth.register"))
        email = User.query.filter_by(email=form.email.data).first()
        if email:
            flash("Email already exists!")
            return redirect(url_for("auth.register"))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, registration successful!")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

        
@bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for password reset instructions.")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)


@bp.route("/change_password/<token>", methods=["GET", "POST"])
def change_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_reset_password_token(token)
    if not user:
        flash("Invalid Token!")
        return redirect(url_for("main.index"))
    form = PasswordChangeForm()
    if form.validate_on_submit():
        new_password = form.password.data
        user.set_password(new_password)
        db.session.commit()
        flash("Password has been reset!")
        return redirect(url_for("auth.login"))
    return render_template("auth/change_password.html", form=form)