from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-posts.user', '-comments.user', '-comments.post.user')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    posts = db.relationship('Post', back_populates='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError('Invalid email address')
        return email

    def set_password(self, password):
        """Hash the password and store it in the password_hash field."""
        self.validate_password_complexity(password)
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def validate_password_complexity(self, password):
        """Ensure the password meets complexity requirements."""
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # Add more complexity rules as needed

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    serialize_rules = ('-user.posts', '-comments.post', '-comments.user.posts')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Post {self.id} - {self.title}>'

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    serialize_rules = ('-user.comments', '-post.comments', '-post.user.comments')

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

    def __repr__(self):
        return f'<Comment {self.id}>'