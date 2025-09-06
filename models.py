from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy() 

# Association table for Post <-> Tag
post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

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
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }
        
    def __repr__(self):
        return f"<User {self.id} - {self.username} - {self.email}>"

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    posts = db.relationship('Post', back_populates='category', cascade='all, delete-orphan')
    tags = db.relationship('Tag', back_populates='category', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        return f"<Category {self.id} - {self.name}>"

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    category = db.relationship('Category', back_populates='tags')
    posts = db.relationship('Post', secondary=post_tags, back_populates='tags')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        return f"<Tag {self.id} - {self.name}>"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    excerpt = db.Column(db.String(500))
    content = db.Column(db.Text, nullable=False)
    featured_image = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    user = db.relationship('User', back_populates='posts')
    category = db.relationship('Category', back_populates='posts')
    tags = db.relationship('Tag', secondary=post_tags, back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "featured_image": self.featured_image,
            "created_at": self.created_at.isoformat(),
            "author": self.user.to_dict() if self.user else None,

            "category": self.category.to_dict() if self.category else None,
            "tags": [tag.to_dict() for tag in self.tags]
        }

    def __repr__(self):
        return f"<Post {self.id} - {self.title}>"

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "author": self.user.to_dict() if self.user else None
        }

    def __repr__(self):
        return f"<Comment {self.id} - Post {self.post_id} - User {self.user_id}>"
