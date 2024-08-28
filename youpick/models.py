
from .db import db

#used chatgpt to convert schemas.sql to models
# db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    # Relationships
    posts = db.relationship('Main', backref='author', lazy=True)
    sent_requests = db.relationship('Request', foreign_keys='Request.request_id', backref='sender', lazy=True)
    received_requests = db.relationship('Request', foreign_keys='Request.receive_id', backref='receiver', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)
    private_messages = db.relationship('Private', foreign_keys='Private.user_id', backref='sender', lazy=True)
    received_private_messages = db.relationship('Private', foreign_keys='Private.recipient_id', backref='recipient', lazy=True)


class Main(db.Model):
    __tablename__ = 'main'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='main_posts')


class Private(db.Model):
    __tablename__ = 'private'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='sent_private_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_private_messages')


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receive_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('request_id', 'receive_id'),
        db.CheckConstraint(status.in_(['pending', 'accepted', 'rejected']))
    )
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[request_id], backref='sent_requests')
    receiver = db.relationship('User', foreign_keys=[receive_id], backref='received_requests')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('main.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    
    # Relationships
    commenter = db.relationship('User', backref='comments')
    message = db.relationship('Main', backref='comments')
