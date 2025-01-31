from faker import Faker
from models import db, User, Post, Comment  
from app import app
from datetime import datetime

fake = Faker()

with app.app_context():
    # delete all data from tables
    db.session.query(Comment).delete()
    db.session.query(Post).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Seed users
    for _ in range(10):
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            role=fake.random_element(elements=('user', 'author')),
            password_hash=fake.password(),
            created_at=fake.date_this_year()
        )
        db.session.add(user)

    db.session.commit()

    # Seed posts
    for _ in range(20):
        post = Post(
            title=fake.sentence(),
            content=fake.text(),
            user_id=fake.random_int(1, 10),  # Assigning a random user as the author
            status=fake.random_element(elements=('published', 'draft')),
            created_at=fake.date_this_year()
        )
        db.session.add(post)

    db.session.commit()

    # Seed comments
    for _ in range(50):
        comment = Comment(
            content=fake.text(),
            user_id=fake.random_int(1, 10),  
            post_id=fake.random_int(1, 20),  
            created_at=fake.date_this_year()
        )
        db.session.add(comment)

    db.session.commit()

    print("Database seeded successfully!")
