from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime
from app import db


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # Converts a query into a paginated collection dictionary.
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
    #User model representing a user in the application.
    #Inherits from PaginatedAPIMixin and UserMixin.
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    sends = db.relationship("Send", backref="author", lazy="dynamic")
    replies = db.relationship("Reply", backref="author", lazy="dynamic")
    avatar_path = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        #Returns a string representation of the user.
        return "<User {}>".format(self.username)

    def set_password(self, password):
        #Sets the password for the user.
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        #Checks if the provided password matches the stored password hash.
        return check_password_hash(self.password_hash, password)

    def posts_count(self):
        #Returns the count of posts made by the user.
        query = sa.select(sa.func.count()).select_from(self.posts.select().subquery())
        return db.session.scalar(query)

    def to_dict(self):
        #Converts the user object to a dictionary.
        return {"id": self.id, "username": self.username}

    def from_dict(self, data, new_user=False):
        #Populates the user object from a dictionary.
        for field in ["username"]:
            if field in data:
                setattr(self, field, data[field])
        if new_user and "password" in data:
            self.set_password(data["password"])


class Send(PaginatedAPIMixin, db.Model):
    #Send model representing a message sent by a user.
    #Inherits from PaginatedAPIMixin.
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    userId = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_userId"))
    labels = db.Column(db.String(140))
    anonymous = db.Column(db.Boolean)


    def __repr__(self):
        #Returns a string representation of the send message.
        return "<Send {}>".format(self.body)

    def posts_count(self):
        #Returns the count of posts related to the send message.
        query = sa.select(sa.func.count()).select_from(self.posts.select().subquery())
        return db.session.scalar(query)

    def to_dict(self):
        # Converts the send object to a dictionary.
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
    #Reply model representing a reply to a send message.
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    userId = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_userId"))
    sendId = db.Column(db.Integer, db.ForeignKey("send.id", name="fk_sendId"))
    anonymous = db.Column(db.Boolean)


    def __repr__(self):
        #Returns a string representation of the reply message.
        return "<Reply {}>".format(self.body)

    def to_dict(self):
        #Converts the reply object to a dictionary.
        return {
            "id": self.id,
            "body": self.body,
            "userId": self.userId,
            "sendId": self.sendId,
            "anonymous": self.anonymous,
        }

    def from_dict(self, data):
        #Populates the reply object from a dictionary.
        id = data.get("id")
        body = data.get("body")
        userId = data.get("userId")
        sendId = data.get("sendId")
        anonymous = data.get("anonymous")
        return Reply(
            id=id, body=body, userId=userId, sendId=sendId, anonymous=anonymous
        )


@login.user_loader
#Loads a user by their ID.
def load_user(id):
    return User.query.get(int(id))
