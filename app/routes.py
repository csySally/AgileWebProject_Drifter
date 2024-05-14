from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app import app, db
from app.forms import LoginForm
from app.models import User, Send, Reply
from flask import request
from urllib.parse import urlparse
from flask import session
from app.forms import RegistrationForm, SendForm, ReplyForm
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os


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
        # Redirect to a default username or handle appropriately
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
            return jsonify({"error": "Invalid username or password"}), 401

        login_user(user)
        return jsonify({"message": "Login successful"}), 200

    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
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
                    "redirect": url_for("login"),
                }
            ),
            200,
        )
    return render_template("register.html", title="Register")


@app.route("/user/<username>/send", methods=["GET", "POST"])
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


@app.route("/user/<username>/reply", methods=["GET", "POST"])
@login_required
def reply(username):
    if current_user.username != username:
        abort(403)
    form = ReplyForm()
    sends = Send.query.order_by(Send.id.desc()).limit(5).all()
    if form.validate_on_submit():
        send = Send.query.get_or_404(form.send_id.data)
        reply = Reply(
            body=form.reply.data,
            author=current_user,
            anonymous=form.anonymous.data,
            sendId=send.id,
        )
        db.session.add(reply)
        db.session.commit()
        flash("Your reply has been posted!")
        return redirect(url_for("user", username=current_user.username))
    return render_template(
        "flask_reply.html",
        title="Reply Message",
        form=form,
        sends=sends,
        user=current_user,
    )


"""  
@app.route('/label', methods=['GET', 'POST'])
@login_required
def label():
    form = LabelForm()
    if form.validate_on_submit():
        label = Labels(label=form.label.data)
        db.session.add(label)
        db.session.commit()       
        flash('Your label has been added!')   
        return redirect(url_for('send'))
    return render_template('flask_label.html', title='Add Label', form=form)"""


@app.route("/upload_image", methods=["POST"])
def upload_image():
    file = request.files["image"]
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        relative_path = os.path.join("uploads", filename)
        current_user.avatar_path = relative_path
        db.session.commit()

        return jsonify({"message": "Image uploaded successfully"}), 200
    return jsonify({"error": "No file uploaded"}), 400
