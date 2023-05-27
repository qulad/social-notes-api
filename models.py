from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class UserLogin(db.Model):
    __bind_key__ = "password_server"
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.Text, nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, pass_):
        return bcrypt.check_password_hash(self.password, pass_)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name = db.Column(db.String(60), nullable=False, unique=True)
    public_profile = db.Column(db.Boolean, nullable=False, default=0)
    country = db.Column(db.String(20), default="", nullable=True)
    biography = db.Column(db.String(120), default="", nullable=True)
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

class Post(db.Model):
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    text = db.Column(db.String(256), nullable=False, default="")
    photo = db.Column(db.Text, nullable=True)
    video = db.Column(db.Text, nullable=True)
    edited = db.Column(db.Boolean, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    edited_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns
            if c.name not in ["created_at", "edited_at"]
        }


class PostUpdated(db.Model):
    post_update_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    old_text = db.Column(db.String(256), nullable=False)
    old_photo = db.Column(db.Text)
    old_video = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

class Block(db.Model):
    block_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    blocker_id = db.Column(db.Integer, nullable=False)
    blocked_id = db.Column(db.Integer, nullable=False)
    since = db.Column(db.DateTime, nullable=False, default=datetime.now())

class Friendship(db.Model): # user_id_1 < user_id_2
    friendship_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id_1 = db.Column(db.Integer, nullable=False)
    user_id_2 = db.Column(db.Integer, nullable=False)
    request_from = db.Column(db.Integer, nullable=False)
    started_at = db.Column(db.DateTime)
    friends = db.Column(db.Boolean, nullable=False, default=False)
    requested_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
    def to_dict(self):
        
        data = {
            c.name: getattr(self, c.name) for c in self.__table__.columns
            if c.name not in ["requested_time", "started_at"]
        }
        if self.started_at is not None:
            data["started_at"] = self.started_at.isoformat()
        return data
