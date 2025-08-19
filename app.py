import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from models import db, User, Post, Comment

app = Flask(__name__)

app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app) 
CORS(app)

# Welcome route
@app.route('/')
def welcome():
    return {"message": "Welcome to Bloppost App!"}, 200

# User Resource
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return user.to_dict(), 200
        else:
            users = User.query.all()
            return [user.to_dict() for user in users], 200

    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return {"error": "Missing required fields"}, 400

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

# Post Resource
class PostResource(Resource):
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get_or_404(post_id)
            return post.to_dict(), 200
        else:
            posts = Post.query.all()
            return [post.to_dict() for post in posts], 200

    def post(self):
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        user_id = data.get('user_id')

        if not title or not content or not user_id:
            return {"error": "Missing required fields"}, 400

        new_post = Post(title=title, content=content, user_id=user_id)
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
            if data['user_id'] is None:
                return {"error": "user_id cannot be null"}, 400
            post.user_id = data['user_id']

        db.session.commit()
        return post.to_dict(), 200

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted successfully"}, 200

# Comment Resource
class CommentResource(Resource):
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get_or_404(post_id)
            comments = Comment.query.filter_by(post_id=post.id).all()
            return [comment.to_dict() for comment in comments], 200
        else:
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

# Adding resources to the API
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(PostResource, '/posts', '/posts/<int:post_id>')
api.add_resource(CommentResource, '/comments', '/posts/<int:post_id>/comments')

if __name__ == '__main__':
    app.run(debug=True, port=5555)