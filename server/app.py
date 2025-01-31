from flask import Flask, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from datetime import datetime
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Post, Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Helper function to validate required fields
def validate_required_fields(data, required_fields):
    if not data or not all(key in data for key in required_fields):
        return make_response({'error': f'Missing required fields: {required_fields}'}, 400)
    return None

# Helper function to check if a post already exists
def post_exists(title, content, user_id):
    return Post.query.filter_by(title=title, content=content, user_id=user_id).first()

class Home(Resource):
    def get(self):
        return {'message': 'Welcome to the Blog Platform'}

api.add_resource(Home, '/')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['username', 'email', 'password', 'role']
    validation_error = validate_required_fields(data, required_fields)
    if validation_error:
        return validation_error

    if User.query.filter_by(email=data['email']).first():
        return make_response({'error': 'Email already registered'}, 400)

    user = User(
        username=data['username'],
        email=data['email'],
        role=data['role'],
        created_at=datetime.utcnow()
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return make_response({'message': 'User registered successfully', 'user': user.to_dict()}, 201)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    required_fields = ['email', 'password']
    validation_error = validate_required_fields(data, required_fields)
    if validation_error:
        return validation_error

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return make_response({'error': 'User not found'}, 404)

    if not user.check_password(data['password']):
        return make_response({'error': 'Invalid password'}, 401)

    return make_response({'message': 'Login successful', 'user': user.to_dict()}, 200)

@app.route('/api/logout', methods=['POST'])
def logout():
    return make_response({'message': 'Logout successful'}, 200)

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    posts = Post.query.all()
    posts_data = [post.to_dict() for post in posts]
    return make_response({'message': 'Dashboard data fetched successfully', 'posts': posts_data}, 200)

@app.route('/api/authors', methods=['GET'])
def get_authors():
    authors = User.query.filter_by(role='author').all()
    authors_data = [author.to_dict() for author in authors]
    return make_response({'message': 'Authors fetched successfully', 'authors': authors_data}, 200)

# CRUD operations for User model using Flask-RESTful
class UserResource(Resource):
    def get(self):
        return make_response([user.to_dict() for user in User.query.all()], 200)
    
    def post(self):
        data = request.get_json()
        required_fields = ['username', 'email', 'password', 'role']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return validation_error

        user = User(username=data['username'], email=data['email'], role=data['role'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return make_response(user.to_dict(), 201)

api.add_resource(UserResource, '/users')

class UserById(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user:
            return make_response(user.to_dict(), 200)
        return make_response({'error': 'User not found'}, 404)
    
    def patch(self, id):
        user = User.query.get(id)
        if user:
            data = request.get_json()
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'password' in data:
                user.set_password(data['password'])
            if 'role' in data:
                user.role = data['role']
            db.session.commit()
            return make_response(user.to_dict(), 200)
        return make_response({'error': 'User not found'}, 404)
    
    def delete(self, id):
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response({'message': 'User deleted successfully'}, 200)
        return make_response({'error': 'User not found'}, 404)

api.add_resource(UserById, '/users/<int:id>')

# CRUD operations for Post model using Flask-RESTful
class PostResource(Resource):
    def get(self):
        return make_response([post.to_dict() for post in Post.query.all()], 200)

    def post(self):
        data = request.get_json()
        required_fields = ['title', 'content', 'user_id']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return validation_error

        user = User.query.get(data['user_id'])
        if not user or user.role != 'author':
            return make_response({'error': 'Unauthorized - Only authors can create posts'}, 403)

        # Check if the post already exists
        if post_exists(data['title'], data['content'], data['user_id']):
            return make_response({'error': 'Post already exists'}, 400)

        post = Post(
            title=data['title'],
            content=data['content'],
            created_at=datetime.utcnow(),
            user_id=data['user_id']
        )
        db.session.add(post)
        db.session.commit()
        return make_response({'message': 'Post created successfully', 'post': post.to_dict()}, 201)

api.add_resource(PostResource, '/posts')

class PostById(Resource):
    def get(self, id):
        post = Post.query.get(id)
        if post:
            return make_response(post.to_dict(), 200)
        return make_response({'error': 'Post not found'}, 404)
    
    def patch(self, id):
        post = Post.query.get(id)
        if post:
            data = request.get_json()
            if 'title' in data:
                post.title = data['title']
            if 'content' in data:
                post.content = data['content']
            db.session.commit()
            return make_response(post.to_dict(), 200)
        return make_response({'error': 'Post not found'}, 404)
    
    def delete(self, id):
        post = Post.query.get(id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return make_response({'message': 'Post deleted successfully'}, 200)
        return make_response({'error': 'Post not found'}, 404)

api.add_resource(PostById, '/posts/<int:id>')

# CRUD operations for Comment model using Flask-RESTful
class CommentResource(Resource):
    def get(self):
        return make_response([comment.to_dict() for comment in Comment.query.all()], 200)

    def post(self):
        data = request.get_json()
        required_fields = ['content', 'user_id', 'post_id']
        validation_error = validate_required_fields(data, required_fields)
        if validation_error:
            return validation_error

        comment = Comment(
            content=data['content'],
            created_at=datetime.utcnow(),
            user_id=data['user_id'],
            post_id=data['post_id']
        )
        db.session.add(comment)
        db.session.commit()
        return make_response({'message': 'Comment created successfully', 'comment': comment.to_dict()}, 201)

api.add_resource(CommentResource, '/comments')

@app.errorhandler(404)
def not_found(error):
    return make_response({'error': 'Not found'}, 404)

if __name__ == '__main__':
    app.run(debug=True, port=5555)