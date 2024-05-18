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

bp = Blueprint('main', __name__)


@bp.route("/")
@bp.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.user", username=current_user.username))
    return redirect(url_for("main.login"))


@bp.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    if username is None:
        # Redirect to a default username or handle appropriately
        return redirect(url_for("main.login"))
    if current_user.username != username:
        abort(403)  # HTTP status code for "Forbidden"
    return render_template("index.html", username=username, user=current_user)


@bp.route("/get_user_info")
@login_required
def get_user_info():
    if current_user.is_authenticated:
        return jsonify(username=current_user.username)
    return jsonify(username="unknown"), 403


@bp.route("/login", methods=["GET", "POST"])
def login():
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
    logout_user()
    return redirect(url_for("main.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
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


@bp.route("/api/random_other_note")
@login_required
def random_other_note():
    all_other_notes = Send.query.filter(Send.userId != current_user.id).all()
    if not all_other_notes:
        return jsonify({"error": "No other notes available"}), 404

    random_note = random.choice(all_other_notes)
    if random_note.anonymous:
        avatar_url = url_for("static", filename="images/default-avatar.png")
    else:
        avatar_url = url_for(
            "static",
            filename=(
                random_note.author.avatar_path
                if random_note.author.avatar_path
                else "images/default-avatar.png"
            ),
        )
    return jsonify(
        {
            "id": random_note.id,
            "body": random_note.body,
            "author": random_note.author.username,
            "anonymous": random_note.anonymous,
            "avatar_url": avatar_url,
        }
    )


@bp.route("/api/random_note_by_label", methods=["GET"])
@login_required
def random_note_by_label():
    label = request.args.get("label", None)
    if label:
        filtered_notes = Send.query.filter(
            Send.userId != current_user.id, Send.labels.ilike(f"%{label}%")
        ).all()
    else:
        filtered_notes = Send.query.filter(Send.userId != current_user.id).all()

    if not filtered_notes:
        return jsonify({"error": "No notes available with the given label"}), 404

    random_note = random.choice(filtered_notes)
    if random_note.anonymous:
        avatar_url = url_for("static", filename="images/default-avatar.png")
    else:
        avatar_url = url_for(
            "static",
            filename=(
                random_note.author.avatar_path
                if random_note.author.avatar_path
                else "images/default-avatar.png"
            ),
        )
    return jsonify(
        {
            "id": random_note.id,
            "body": random_note.body,
            "author": random_note.author.username,
            "anonymous": random_note.anonymous,
            "avatar_url": avatar_url,
        }
    )


@bp.route("/reply-note")
@login_required
def reply_note():
    return render_template("reply_note_entry.html", user=current_user)


@bp.route("/reply-note-random")
@login_required
def reply_note_random():
    return render_template("reply_random.html", user=current_user)


@bp.route("/reply-note-check")
@login_required
def reply_note_check():
    label = request.args.get("label", None)
    return render_template("check_and_reply.html", user=current_user, label=label)


@bp.route("/check-my-reply")
@login_required
def check_my_reply():
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


@bp.route("/api/user/<username>/notes_with_replies")
@login_required
def api_get_notes_with_replies(username):
    if current_user.username != username:
        abort(403)

    user_notes = Send.query.filter_by(userId=current_user.id).all()
    notes_with_replies = []
    for note in user_notes:
        replies = Reply.query.filter_by(sendId=note.id).all()
        notes_with_replies.append(
            {"note": note.to_dict(), "replies": [reply.to_dict() for reply in replies]}
        )

    return jsonify(notes_with_replies=notes_with_replies)


@bp.route("/user/<username>/reply", methods=["GET", "POST"])
@login_required
def reply(username):
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


@bp.route("/user/<username>/sent_notes")
@login_required
def sent_notes(username):
    if current_user.username != username:
        abort(403)

    user_notes = Send.query.filter_by(userId=current_user.id).all()
    notes_with_replies = []
    for note in user_notes:
        replies = Reply.query.filter_by(sendId=note.id).all()
        notes_with_replies.append(
            {
                "note": note.to_dict(),  
                "replies": [reply.to_dict() for reply in replies],
            }
        )

    return jsonify(notes_with_replies=notes_with_replies)


@bp.route(
    "/api/user/<username>/note/<int:note_id>/reply/<int:reply_id>", methods=["GET"]
)
@login_required
def api_note_reply_detail(username, note_id, reply_id):
    if current_user.username != username:
        abort(403)
    note = Send.query.get_or_404(note_id)
    reply = Reply.query.get_or_404(reply_id)
    user = User.query.get(reply.userId)

    note_data = {
        "id": note.id,
        "body": note.body,
        "anonymous": note.anonymous,
        "labels": note.labels,
    }

    reply_data = {
        "id": reply.id,
        "body": reply.body,
        "from_user": (
            User.query.get(reply.userId).username
            if not reply.anonymous
            else "Anonymous"
        ),
        "anonymous": reply.anonymous,
        "avatar_path": (
            user.avatar_path if user.avatar_path else "images/default-avatar.png"
        ),
    }

    return jsonify({"note": note_data, "reply": reply_data})


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
