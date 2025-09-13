import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from sqlalchemy.orm import joinedload
from models import db, User, Post, Comment, Category, Tag
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit
app.json.compact = False

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)

# Ensure upload directory exists at startup
with app.app_context():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    print(f"Upload directory ensured: {app.config['UPLOAD_FOLDER']}")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def welcome():
    return {"message": "Welcome to Blogpost App!"}, 200

# Add authentication routes
@app.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json()
    login_identifier = data.get('identifier')  # Unified field name
    password = data.get('password')
    
    if not login_identifier or not password:
        return jsonify({"error": "Email/username and password required"}), 400
    
    # Find user by email OR username
    user = User.query.filter(
        (User.email == login_identifier) | (User.username == login_identifier)
    ).first()
    
    if not user:
        return jsonify({"error": "Invalid email/username or password"}), 401
    
    try:
        if not user.check_password(password):
            return jsonify({"error": "Invalid email/username or password"}), 401
    except Exception as e:
        print(f"Password check error: {str(e)}")
        return jsonify({"error": "Authentication error"}), 500
    
    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "token": "demo_token_123"  # Replace with JWT later
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
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "User created successfully",
        "user": new_user.to_dict()
    }), 201

# New file upload endpoint
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            # Create upload directory if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Save file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Return URL
            image_url = f"/static/uploads/{unique_filename}"
            return jsonify({
                'url': image_url,
                'message': 'File uploaded successfully'
            }), 200
            
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return jsonify({'error': 'Failed to upload file'}), 500
    
    return jsonify({'error': 'Invalid file type. Allowed types: PNG, JPG, JPEG, GIF, WEBP'}), 400

# Serve uploaded files
@app.route('/static/uploads/<filename>')
def serve_uploaded_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

# Keep the old upload endpoint for backward compatibility
@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.files.get('image')
    if not image:
        return {"error": "No image provided"}, 400  
    
    if not allowed_file(image.filename):
        return {"error": "Invalid file type"}, 400
        
    filename = secure_filename(image.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    
    # Create directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    image.save(upload_path)
    
    return {"url": f"/static/uploads/{unique_filename}"}, 201

# my-posts endpoint
@app.route('/posts/my-posts', methods=['GET', 'OPTIONS'])
def get_my_posts():
    if request.method == 'OPTIONS':
        return '', 200  # Handle preflight request

    user_id = request.args.get('user_id')  # frontend should pass ?user_id=...
    if not user_id:
        return jsonify({"error": "User ID required"}), 400

    try:
        posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
        return jsonify([post.to_dict() for post in posts]), 200
    except Exception as e:
        print(f"Error fetching my posts: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


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
        try:
            data = request.get_json()
            print("Received post data:", data)  # Debug logging

            title = data.get('title')
            content = data.get('content')
            excerpt = data.get('excerpt')
            user_id = data.get('user_id')
            category_id = data.get('category_id')
            featured_image = data.get('featured_image')
            tag_ids = data.get('tag_ids')

            # ===== Required field checks =====
            if not title:
                return {"error": "Title is required"}, 400
            if not content:
                return {"error": "Content is required"}, 400
            if not excerpt:
                return {"error": "Excerpt is required"}, 400
            if not user_id:
                return {"error": "User ID is required"}, 400
            if not category_id:
                return {"error": "Category ID is required"}, 400
            if not tag_ids or not isinstance(tag_ids, list) or len(tag_ids) == 0:
                return {"error": "At least one tag is required"}, 400

            # ===== Validate user exists =====
            user = User.query.get(user_id)
            if not user:
                return {"error": f"User with ID {user_id} not found"}, 404

            # ===== Validate category exists =====
            try:
                category_id = int(category_id)
                category = Category.query.get(category_id)
                if not category:
                    return {"error": f"Category with ID {category_id} not found"}, 404
            except (ValueError, TypeError):
                return {"error": "Invalid category ID format"}, 400

            # ===== Validate tags exist =====
            try:
                tag_ids = [int(tag_id) for tag_id in tag_ids]
                existing_tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
                if len(existing_tags) != len(tag_ids):
                    return {"error": "One or more tags not found"}, 404
            except (ValueError, TypeError):
                return {"error": "Invalid tag IDs format"}, 400

            # ===== Create the post =====
            new_post = Post(
                title=title,
                content=content,
                excerpt=excerpt,
                user_id=user_id,
                category_id=category_id,
                featured_image=featured_image
            )

            # Attach tags
            tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            new_post.tags.extend(tags)

            db.session.add(new_post)
            db.session.commit()

            return new_post.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            print(f"Error creating post: {str(e)}")
            import traceback; traceback.print_exc()
            return {"error": "Internal server error", "details": str(e)}, 500


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
    # Ensure upload directory exists before running
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    print(f"Server starting with upload directory: {app.config['UPLOAD_FOLDER']}")
    app.run(debug=True, port=5555)