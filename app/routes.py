from flask import render_template, redirect, url_for, jsonify, abort
from flask import current_app
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app import db
from app.forms import LoginForm
from app.models import User, Send, Reply
from flask import request
from urllib.parse import urlparse
from flask import session
from app.forms import RegistrationForm, SendForm, ReplyForm
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
import random
from flask import Blueprint

# Blueprint for web routes
bp = Blueprint('main', __name__)

@bp.route("/")
@bp.route("/index")
def index():
    # Redirects authenticated users to their user page and unauthenticated users to the login page.
    if current_user.is_authenticated:
        return redirect(url_for("main.user", username=current_user.username))
    return redirect(url_for("main.login"))

@bp.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    # Displays the user's main page. Redirects to the login page if the username is not provided or does not match the current user.
    if username is None:
        # Redirect to a default username or handle appropriately
        return redirect(url_for("main.login"))
    if current_user.username != username:
        abort(403)  # HTTP status code for "Forbidden"
    return render_template("index.html", username=username, user=current_user)

@bp.route("/get_user_info")
@login_required
def get_user_info():
    # Returns the username of the currently authenticated user as JSON.
    if current_user.is_authenticated:
        return jsonify(username=current_user.username)
    return jsonify(username="unknown"), 403

@bp.route("/login", methods=["GET", "POST"])
def login():
    # Handles user login. Redirects authenticated users to the index page.
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return jsonify({"error": "Invalid username or password"}), 401

        login_user(user)
        return jsonify({"message": "Login successful"}), 200

    return render_template("login.html")

@bp.route("/logout", methods=["POST"])
def logout():
    # Logs out the current user and redirects to the login page.
    logout_user()
    return redirect(url_for("main.login"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    # Handles user registration. Registers a new user if they are not already logged in.
    if current_user.is_authenticated:
        return jsonify({"status": "error", "message": "Already logged in"}), 400

    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return (
                jsonify({"status": "error", "message": "Missing username or password"}),
                400,
            )
        user = User.query.filter_by(username=username).first()
        if user:
            return (
                jsonify({"status": "error", "message": "Username already exists"}),
                409,
            )
        new_user = User(
            username=username, password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Registration successful",
                    "redirect": url_for("main.login"),
                }
            ),
            200,
        )
    return render_template("register.html", title="Register")

@bp.route("/user/<username>/send", methods=["GET", "POST"])
@login_required
def send(username):
    # Allows the user to send a message. If the user is not authorized, returns a 403 status code.
    if current_user.username != username:
        abort(403)  # HTTP status code for "Forbidden"
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        send = Send(
            body=data.get("note"),
            author=current_user,
            anonymous=data.get("anonymous"),
            labels=data.get("labels"),
        )
        db.session.add(send)
        db.session.commit()
        return jsonify({"message": "Your message has been sent!"}), 200
    return render_template("add_note.html", title="Send Message", user=current_user)

@bp.route("/user/<username>/reply", methods=["GET", "POST"])
@login_required
def reply(username):
    #Processes the reply submission and stores it in the database.
    if current_user.username != username:
        abort(403)

    data = request.get_json()
    if not data or "note_id" not in data or "reply_body" not in data:
        return jsonify({"error": "Missing data"}), 400

    note_id = data["note_id"]
    reply_body = data["reply_body"]
    anonymous = data.get("anonymous", False)

    note = Send.query.get_or_404(note_id)
    reply = Reply(
        body=reply_body,
        userId=current_user.id,
        sendId=note.id,
        anonymous=anonymous,
    )

    db.session.add(reply)
    db.session.commit()

    return jsonify({"message": "Reply successfully posted"}), 200

@bp.route("/reply-note")
@login_required
def reply_note():
    return render_template("reply_note_entry.html", user=current_user)

@bp.route("/reply-note-random")
@login_required
def reply_note_random():
    # Renders the reply random note page.
    return render_template("reply_random.html", user=current_user)

@bp.route("/reply-note-check")
@login_required
def reply_note_check():
    # Renders the check and reply page for notes with a specified label.
    label = request.args.get("label", None)
    return render_template("check_and_reply.html", user=current_user, label=label)

@bp.route("/check-my-reply")
@login_required
def check_my_reply():
    # Renders the page to check replies to the user's notes.
    user_notes = Send.query.filter_by(userId=current_user.id).all()
    notes_with_replies = []
    for note in user_notes:
        replies = Reply.query.filter_by(sendId=note.id).all()
        note_with_replies = {"note": note, "replies": replies}
        notes_with_replies.append(note_with_replies)

        for reply in replies:
            print(note.id, reply.id)

    return render_template(
        "check_reply.html", user=current_user, notes=notes_with_replies
    )

@bp.route("/user/<username>/note/<int:note_id>/reply/<int:reply_id>", methods=["GET"])
@login_required
def note_reply_detail(username, note_id, reply_id):
    if current_user.username != username:
        abort(403)
    note = Send.query.get_or_404(note_id)
    reply = Reply.query.get_or_404(reply_id)

    return render_template("open_note_answer.html", note=note, reply=reply)

@bp.route("/upload_image", methods=["POST"])
def upload_image():
    file = request.files["image"]
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        relative_path = os.path.normpath(os.path.join("uploads", filename)).replace(
            "\\", "/"
        )
        current_user.avatar_path = relative_path
        db.session.commit()

        return jsonify({"message": "Image uploaded successfully"}), 200
    return jsonify({"error": "No file uploaded"}), 400

