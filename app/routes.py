from flask import render_template, redirect, url_for, flash, jsonify, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm
from app.models import User
from werkzeug.security import generate_password_hash
import os
import random

@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("user", username=current_user.username))
    return redirect(url_for("login"))

@app.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    if username is None:
        return redirect(url_for("login"))
    if current_user.username != username:
        abort(403)  # HTTP status code for "Forbidden"
    return render_template("index.html", username=username, user=current_user)

@app.route("/get_user_info")
@login_required
def get_user_info():
    if current_user.is_authenticated:
        return jsonify(username=current_user.username)
    return jsonify(username="unknown"), 403

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return "Invalid username or password", 401

        login_user(user)
        return "Login successful", 200

    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return "Already logged in", 400

    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return "Missing username or password", 400

        user = User.query.filter_by(username=username).first()
        if user:
            return "Username already exists", 409

        new_user = User(
            username=username, password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        return "Registration successful", 200

    return render_template("register.html", title="Register")
