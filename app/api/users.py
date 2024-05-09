from app.api import bp
from app.models import User, Send, Reply
from app import db
import sqlalchemy as sa
from flask import request
from flask import url_for
from app.api.errors import bad_request

@bp.route('/users/<int:id>', methods=['GET'])
def get_user_byID(id):
    return db.get_or_404(User, id).to_dict()

@bp.route('/users', methods=['GET'])
def get_users():
    users_query = sa.select(User)
    users = db.session.execute(users_query).scalars().all()
    users_data = [user.to_dict() for user in users]
    return users_data

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        return bad_request('must include username and password fields')
      
    if db.session.scalar(sa.select(User).where(User.username == data['username'])):
        return bad_request('please use a different username')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()

    return user.to_dict(), 201, {'Location': url_for('api.get_user',
                                                     id=user.id)}

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass

@bp.route('/users/<int:id>/send', methods=['GET'])
def get_user_send(id):
    user = User.query.get(id)
    if not user:
        return bad_request('User not found')
    sends_query = sa.select(Send).where(Send.userId == user.id)
    sends = db.session.execute(sends_query).scalars().all()
    sends_data = [send.to_dict() for send in sends]
    return sends_data


@bp.route('/users/<int:id>/send', methods=['POST'])
def create_send(id):
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

    return user.to_dict(), 201, {'Location': url_for('api.get_user_send',
                                                     id=user.id)}
    
    
@bp.route('/users/<int:id>/reply', methods=['GET'])
def get_user_reply(id):
    user = User.query.get(id)
    if not user:
        return bad_request('User not found')
    reply_query = sa.select(Reply).where(Reply.userId == user.id)
    replys = db.session.execute(reply_query).scalars().all()
    reply_data = [reply.to_dict() for reply in replys]
    return reply_data


@bp.route('/users/<int:user_id>/reply', methods=['POST'])
def create_reply(user_id):
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
