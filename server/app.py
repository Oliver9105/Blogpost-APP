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

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    # Example: Fetch posts for the logged-in user
    # You can customize this based on your application's requirements
    posts = Post.query.all()  # Fetch all posts (or filter by user_id if needed)
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
        user = User(username=data['username'], email=data['email'], role=data['role'])
        user.set_password(data['password'])  # Hash the password
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
                user.set_password(data['password'])  # Hash the new password
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

        # Add authorization check
        user = User.query.get(data.get('user_id'))
        if not user or user.role != 'author':
            return make_response({'error': 'Unauthorized - Only authors can create posts'}, 403)

        # Existing post creation logic
        post = Post(
            title=data['title'],
            content=data['content'],
            created_at=datetime.utcnow(),
            user_id=data['user_id']
        )
        db.session.add(post)
        db.session.commit()
        return make_response(post.to_dict(), 201)

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
        comment = Comment(content=data['content'], created_at=datetime.utcnow(), user_id=data['user_id'], post_id=data['post_id'])
        db.session.add(comment)
        db.session.commit()
        return make_response(comment.to_dict(), 201)

api.add_resource(CommentResource, '/comments')

@app.errorhandler(404)
def not_found(error):
    return make_response({'error': 'Not found'}, 404)

if __name__ == '__main__':
    app.run(debug=True, port=555



