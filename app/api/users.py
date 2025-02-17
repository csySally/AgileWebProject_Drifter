from app.api import bp
from app.models import User, Send, Reply
from app import db
import sqlalchemy as sa
from flask import request,jsonify, url_for
from flask import url_for
from app.api.errors import bad_request
import random
from flask_login import login_required, current_user


@bp.route('/users/<int:id>', methods=['GET'])
def get_user_byID(id):
    # Retrieve a user by their ID.
    return db.get_or_404(User, id).to_dict()

@bp.route('/users', methods=['GET'])
def get_users():
    # Retrieve all users.
    users_query = sa.select(User)
    users = db.session.execute(users_query).scalars().all()
    users_data = [user.to_dict() for user in users]
    return users_data

@bp.route('/users', methods=['POST'])
def create_user():
    # Create a new user.
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        return bad_request('must include username and password fields')
      
    if db.session.scalar(sa.select(User).where(User.username == data['username'])):
        return bad_request('please use a different username')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()

    return user.to_dict(), 201, {'Location': url_for('api.get_user_byID', id=user.id)}

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass

@bp.route('/users/<int:id>/send', methods=['GET'])
def get_user_send(id):
    # Retrieve all messages (sends) sent by a user.
    user = User.query.get(id)
    if not user:
        return bad_request('User not found')
    sends_query = sa.select(Send).where(Send.userId == user.id)
    sends = db.session.execute(sends_query).scalars().all()
    sends_data = [send.to_dict() for send in sends]
    return sends_data

@bp.route('/users/<int:id>/send', methods=['POST'])
def create_send(id):
    # Create a new message (send) for a user.
    user = User.query.get(id)
    if not user:
        return bad_request('can not find user with id')
    data = request.get_json()

    if 'body' not in data:
        return bad_request('must include message field')
      
    send = Send(userId=id, body=data['body'], labels=data['labels'], anonymous=data['anonymous'])
    send.from_dict(data)
    db.session.add(send)
    db.session.commit()

    return send.to_dict(), 201, {'Location': url_for('api.get_user_send', id=user.id)}
    
@bp.route('/users/<int:id>/reply', methods=['GET'])
def get_user_reply(id):
    # Retrieve all replies made by a user.
    user = User.query.get(id)
    if not user:
        return bad_request('User not found')
    reply_query = sa.select(Reply).where(Reply.userId == user.id)
    replies = db.session.execute(reply_query).scalars().all()
    reply_data = [reply.to_dict() for reply in replies]
    return reply_data

@bp.route('/users/<int:user_id>/reply', methods=['POST'])
def create_reply(user_id):
    # Create a new reply to a message (send) for a user.
    user = User.query.get(user_id)
    
    if not user:
        return bad_request('can not find user with id')

    data = request.get_json()

    if 'send_id' not in data:
        return bad_request('must include send_id field')

    send_id = data['send_id']
    send = Send.query.get(send_id)

    if not send:
        return bad_request('can not find send with id')

    if 'body' not in data:
        return bad_request('must include body field')

    reply = Reply(userId=user_id, body=data['body'], sendId=send_id, anonymous=data['anonymous'])
    reply.from_dict(data)
    db.session.add(reply)
    db.session.commit()

    return reply.to_dict(), 201, {'Location': url_for('api.get_user_reply', id=user.id)}


@bp.route('/random_other_note', methods=['GET'])
@login_required
def random_other_note():
    # Returns a random note from other users as JSON. If no notes are available, returns a 404 status code.
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
    
@bp.route("/random_note_by_label", methods=["GET"])
@login_required
def random_note_by_label():
    #Returns a random note filtered by the specified label as JSON. If no notes are available, returns a 404 status code
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
    
@bp.route("/user/<username>/notes_with_replies")
@login_required
def get_notes_with_replies(username):
    #Returns the user's notes with their replies as JSON. If the current user is not authorized, returns a 403 status code.
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


@bp.route(
    "/user/<username>/note/<int:note_id>/reply/<int:reply_id>", methods=["GET"]
)
@login_required
def note_reply_detail(username, note_id, reply_id):
    if current_user.username != username:
        abort(403)
    
    note = db.session.get(Send, note_id)
    if note is None:
        abort(404)
    
    reply = db.session.get(Reply, reply_id)
    if reply is None:
        abort(404)
    
    user = db.session.get(User, reply.userId)
    if user is None:
        abort(404)

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
            user.username if not reply.anonymous else "Anonymous"
        ),
        "anonymous": reply.anonymous,
        "avatar_path": (
            user.avatar_path if user.avatar_path else "images/default-avatar.png"
        ),
    }

    return jsonify({"note": note_data, "reply": reply_data})