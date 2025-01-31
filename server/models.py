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
    email = db.Column(db.String(120), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)   

    created_at = db.Column(db.DateTime, nullable=False)

    # Relationships
    posts = db.relationship('Post', back_populates='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError('Invalid email address')
        return     
   
     
    def set_password(self, password):
        """Hash the password and store it in the password_hash field."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    
    
