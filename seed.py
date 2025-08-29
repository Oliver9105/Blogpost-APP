from faker import Faker
from models import db, User, Post, Comment, Category, Tag
from app import app
from werkzeug.security import generate_password_hash

fake = Faker()

# Category → Tags mapping
categories_data = {
    "Technology": ["React", "JavaScript", "Web Development", "AI"],
    "Business": ["Startup", "Marketing", "Finance", "Productivity"],
    "Design": ["UI/UX", "Graphic Design", "Branding"],
    "Lifestyle": ["Health", "Travel", "Food", "Fitness"]
}

with app.app_context():
    # Clear existing data
    db.session.query(Comment).delete()
    db.session.query(Post).delete()
    db.session.query(Tag).delete()
    db.session.query(Category).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Seed Users
    users = []
    for _ in range(10):
        password = fake.password(length=10)
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            password_hash=generate_password_hash(password),
            created_at=fake.date_this_year()
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # Seed Categories and Tags
    categories = []
    tags = []
    for cat_name, tag_list in categories_data.items():
        category = Category(name=cat_name)
        db.session.add(category)
        db.session.commit()
        categories.append(category)

        for tag_name in tag_list:
            tag = Tag(name=tag_name, category_id=category.id)
            db.session.add(tag)
            tags.append(tag)
    db.session.commit()

    # Seed Posts
    posts = []
    for _ in range(20):
        user = fake.random_element(users)
        category = fake.random_element(categories)
        post = Post(
            title=fake.sentence(nb_words=6),
            content=fake.paragraph(nb_sentences=5),
            featured_image=fake.image_url(width=800, height=600),
            user_id=user.id,
            category_id=category.id,
            created_at=fake.date_this_year()
        )
        db.session.add(post)
        posts.append(post)
    db.session.commit()

    # Assign random tags to posts
    for post in posts:
        post.tags = fake.random_elements(elements=tags, length=fake.random_int(min=1, max=4), unique=True)
    db.session.commit()

    # Seed Comments
    for _ in range(50):
        comment = Comment(
            content=fake.paragraph(nb_sentences=2),
            user_id=fake.random_element(users).id,
            post_id=fake.random_element(posts).id,
            created_at=fake.date_this_year()
        )
        db.session.add(comment)
    db.session.commit()

    print(f"✅ Seeded {len(users)} users, {len(categories)} categories, {len(tags)} tags, {len(posts)} posts, and 50 comments.")
