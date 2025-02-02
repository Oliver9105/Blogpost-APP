from faker import Faker
from models import db, User, Post, Comment
from app import app
from werkzeug.security import generate_password_hash  # To hash passwords

fake = Faker()

with app.app_context():
    # Clear all data from tables to ensure a fresh seed
    db.session.query(Comment).delete()
    db.session.query(Post).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Seed users
    for _ in range(10):
        password = fake.password()  # Generate a fake password
        hashed_password = generate_password_hash(password)  # Hash the password
        
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            password_hash=hashed_password,  # Use the hashed password
            created_at=fake.date_this_year()  
        )
        db.session.add(user)

    db.session.commit()

    # Seed posts
    for _ in range(20):
        post = Post(
            title=fake.sentence(),
            content=fake.text(),
            user_id=fake.random_int(1, 10), 
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
