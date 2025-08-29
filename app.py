import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from sqlalchemy.orm import joinedload
from models import db, User, Post, Comment, Category, Tag

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///blogpost.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)

@app.route('/')
def welcome():
    return {"message": "Welcome to Blogpost App!"}, 200

# Add authentication routes
@app.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    
    if not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "token": "demo_token_123"
    }), 200
    
@app.route('/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 200
    
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({"error": "Username, email and password required"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)  # Assuming you have a set_password method
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "User created successfully",
        "user": new_user.to_dict()
    }), 201
    
    
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return user.to_dict(), 200
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return {"error": "Missing required fields"}, 400

        if User.query.filter_by(email=email).first():
            return {"error": "Email already registered"}, 409

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

    def patch(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return user.to_dict(), 200

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200

class PostResource(Resource):
    def get(self, post_id=None):
        if post_id:
            post = Post.query.options(joinedload(Post.user)).get_or_404(post_id)
            return post.to_dict(), 200
        posts = Post.query.options(joinedload(Post.user)).order_by(Post.created_at.desc()).all()
        return [post.to_dict() for post in posts], 200

    def post(self):
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        user_id = data.get('user_id')
        category_id = data.get('category_id')
        featured_image = data.get('featured_image')
        tag_ids = data.get('tag_ids', [])

        if not title or not content or not user_id:
            return {"error": "Missing required fields"}, 400

        new_post = Post(
            title=title,
            content=content,
            user_id=user_id,
            category_id=category_id,
            featured_image=featured_image
        )

        if tag_ids:
            tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            new_post.tags.extend(tags)

        db.session.add(new_post)
        db.session.commit()
        return new_post.to_dict(), 201

    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)
        data = request.get_json()

        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        if 'user_id' in data:
            post.user_id = data['user_id']
        if 'category_id' in data:
            post.category_id = data['category_id']
        if 'featured_image' in data:
            post.featured_image = data['featured_image']
        if 'tag_ids' in data:
            post.tags = Tag.query.filter(Tag.id.in_(data['tag_ids'])).all()

        db.session.commit()
        return post.to_dict(), 200

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted successfully"}, 200

class CommentResource(Resource):
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get_or_404(post_id)
            comments = Comment.query.filter_by(post_id=post.id).all()
            return [comment.to_dict() for comment in comments], 200
        comments = Comment.query.all()
        return [comment.to_dict() for comment in comments], 200

    def post(self, post_id):
        data = request.get_json()
        content = data.get('content')
        user_id = data.get('user_id')

        if not content or not user_id:
            return {"error": "Missing required fields"}, 400

        new_comment = Comment(content=content, user_id=user_id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment.to_dict(), 201

class CategoryResource(Resource):
    def get(self, category_id=None):
        if category_id:
            category = Category.query.get_or_404(category_id)
            return category.to_dict(), 200
        categories = Category.query.all()
        return [cat.to_dict() for cat in categories], 200

    def post(self):
        data = request.get_json()
        name = data.get('name')
        if not name:
            return {"error": "Name is required"}, 400
        if Category.query.filter_by(name=name).first():
            return {"error": "Category already exists"}, 409
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category.to_dict(), 201

class TagResource(Resource):
    def get(self, tag_id=None):
        if tag_id:
            tag = Tag.query.get_or_404(tag_id)
            return tag.to_dict(), 200
        tags = Tag.query.all()
        return [t.to_dict() for t in tags], 200

    def post(self):
        data = request.get_json()
        name = data.get('name')
        category_id = data.get('category_id')
        if not name or not category_id:
            return {"error": "Name and category_id are required"}, 400
        if Tag.query.filter_by(name=name).first():
            return {"error": "Tag already exists"}, 409
        tag = Tag(name=name, category_id=category_id)
        db.session.add(tag)
        db.session.commit()
        return tag.to_dict(), 201

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(PostResource, '/posts', '/posts/<int:post_id>')
api.add_resource(CommentResource, '/comments', '/posts/<int:post_id>/comments')
api.add_resource(CategoryResource, '/categories', '/categories/<int:category_id>')
api.add_resource(TagResource, '/tags', '/tags/<int:tag_id>')

if __name__ == '__main__':
    app.run(debug=True, port=5555)
