from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # Add password hashing
from models import db, User, Post, Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

class Home(Resource):
    def get(self):
        return {'message': 'Welcome to the Blog Platform'}

api.add_resource(Home, '/')

@app.route('/api/register', methods=['POST'])
def register():
    # Get data from the request
    data = request.get_json()

    # Validate required fields
    if not data or not all(key in data for key in ['username', 'email', 'password', 'role']):
        return make_response({'error': 'Missing required fields'}, 400)

    # Check if the email is already registered
    if User.query.filter_by(email=data['email']).first():
        return make_response({'error': 'Email already registered'}, 400)

    # Create a new user
    user = User(
        username=data['username'],
        email=data['email'],
        role=data['role'],
        created_at=datetime.utcnow()
    )

    # Hash the password
    user.set_password(data['password'])

    # Save the user to the database
    db.session.add(user)
    db.session.commit()

    # Return a success response
    return make_response({'message': 'User registered successfully', 'user': user.to_dict()}, 201)

@app.route('/api/login', methods=['POST'])
def login():
    # Get data from the request
    data = request.get_json()

    # Validate required fields
    if not data or not all(key in data for key in ['email', 'password']):
        return make_response({'error': 'Missing email or password'}, 400)

    # Find the user by email
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return make_response({'error': 'User not found'}, 404)

    # Verify the password
    if not user.check_password(data['password']):
        return make_response({'error': 'Invalid password'}, 401)

    # Return a success response (you can include a token or user data here)
    return make_response({'message': 'Login successful', 'user': user.to_dict()}, 200)

@app.route('/api/logout', methods=['POST'])
def logout():
  
    return make_response({'message': 'Logout successful'}, 200)

