from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime
from app import db


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = db.paginate(query, page=page, per_page=per_page, error_out=False)
        data = {
            "items": [item.to_dict() for item in resources.items],
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total_pages": resources.pages,
                "total_items": resources.total,
            },
            "_links": {
                "self": url_for(endpoint, page=page, per_page=per_page, **kwargs),
                "next": (
                    url_for(endpoint, page=page + 1, per_page=per_page, **kwargs)
                    if resources.has_next
                    else None
                ),
                "prev": (
                    url_for(endpoint, page=page - 1, per_page=per_page, **kwargs)
                    if resources.has_prev
                    else None
                ),
            },
        }
        return data


class User(PaginatedAPIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    sends = db.relationship("Send", backref="author", lazy="dynamic")
    replies = db.relationship("Reply", backref="author", lazy="dynamic")
    avatar_path = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def posts_count(self):
        query = sa.select(sa.func.count()).select_from(self.posts.select().subquery())
        return db.session.scalar(query)

    def to_dict(self):
        return {"id": self.id, "username": self.username}

    def from_dict(self, data, new_user=False):
        for field in ["username"]:
            if field in data:
                setattr(self, field, data[field])
        if new_user and "password" in data:
            self.set_password(data["password"])


class Send(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    userId = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_userId"))
    labels = db.Column(db.String(140))
    anonymous = db.Column(db.Boolean)

    # user = db.relationship('User', back_populates='sends')
    def __repr__(self):
        return "<Send {}>".format(self.body)

    def posts_count(self):
        query = sa.select(sa.func.count()).select_from(self.posts.select().subquery())
        return db.session.scalar(query)

    def to_dict(self):
        return {
            "id": self.id,
            "body": self.body,
            "userId": self.userId,
            "labels": self.labels,
            "anonymous": self.anonymous,
        }

    def from_dict(self, data):
        id = data.get("id")
        body = data.get("body")
        userId = data.get("userId")
        labels = data.get("labels")
        anonymous = data.get("anonymous")
        return Send(id=id, body=body, userId=userId, labels=labels, anonymous=anonymous)


class Reply(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    userId = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_userId"))
    sendId = db.Column(db.Integer, db.ForeignKey("send.id", name="fk_sendId"))
    anonymous = db.Column(db.Boolean)

    # user = db.relationship('User', back_populates='replies')
    def __repr__(self):
        return "<Reply {}>".format(self.body)

    def to_dict(self):
        return {
            "id": self.id,
            "body": self.body,
            "userId": self.userId,
            "sendId": self.sendId,
            "anonymous": self.anonymous,
        }

    def from_dict(self, data):
        id = data.get("id")
        body = data.get("body")
        userId = data.get("userId")
        sendId = data.get("sendId")
        anonymous = data.get("anonymous")
        return Reply(
            id=id, body=body, userId=userId, sendId=sendId, anonymous=anonymous
        )


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
