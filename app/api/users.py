from app.api import bp
from app.models import User, Send
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