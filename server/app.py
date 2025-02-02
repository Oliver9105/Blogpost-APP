from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Post, Comment

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)
migrate = Migrate(app, db)

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Route to get a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# Route to create a new user (Signup)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')  # Add password field for user creation

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)  # Hash the password before saving
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

# Route to update a user
@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:  # Allow password updates
        user.set_password(data['password'])

    db.session.commit()
    return jsonify(user.to_dict()), 200

# Route to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# Route to get all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])

# Route to get a specific post by ID
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict()), 200

# Route to create a new post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('user_id')

    if not title or not content or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 201

# Route to update a post
@app.route('/posts/<int:post_id>', methods=['PATCH'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()

    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'user_id' in data:
        if data['user_id'] is None:
            return jsonify({"error": "user_id cannot be null"}), 400
        post.user_id = data['user_id']

    db.session.commit()
    return jsonify(post.to_dict()), 200

# Route to delete a post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"}), 200

# Route to get all comments for a specific post
@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).all()
    return jsonify([comment.to_dict() for comment in comments])

# Route to add a comment to a post
@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.get_json()
    content = data.get('content')
    user_id = data.get('user_id')

    if not content or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    new_comment = Comment(content=content, user_id=user_id, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(new_comment.to_dict()), 201

# Route to get all comments
@app.route('/comments', methods=['GET'])
def get_all_comments():
    comments = Comment.query.all()
    return jsonify([comment.to_dict() for comment in comments])

if __name__ == '__main__':
    app.run(debug=True, port=5555)