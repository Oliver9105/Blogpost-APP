from faker import Faker
from models import db, User, Post, Comment, Category, Tag
from app import app
from werkzeug.security import generate_password_hash

fake = Faker()

# --- Category → Tags mapping ---
categories_data = {
    "Technology": [
        "React", "JavaScript", "Web Development", "AI", "Machine Learning",
        "Python", "Data Science", "Cloud Computing", "Cybersecurity", "DevOps"
    ],
    "Business": [
        "Startup", "Marketing", "Finance", "Productivity", "Entrepreneurship",
        "Leadership", "Management", "Investing", "Economics", "Strategy"
    ],
    "Design": [
        "UI/UX", "Graphic Design", "Branding", "Typography", "Illustration",
        "Animation", "Adobe Photoshop", "Adobe Illustrator", "Product Design", "Visual Identity"
    ],
    "Lifestyle": [
        "Health", "Travel", "Food", "Fitness", "Wellness",
        "Mindfulness", "Photography", "Hobbies", "Fashion", "Home Decor"
    ]
}

# --- Predefined sentences for realistic content ---
category_sentences = {
    "Technology": [
        "React is a powerful JavaScript library for building user interfaces.",
        "AI is transforming the way we approach problem-solving in tech.",
        "Web development trends are evolving rapidly in 2025.",
        "Cloud computing allows scalable and flexible applications.",
        "Cybersecurity is crucial for modern online systems.",
        "Machine learning enables computers to learn from data.",
        "Python is one of the most versatile programming languages.",
        "Data science drives insights for better decision-making."
    ],
    "Business": [
        "Effective leadership can drive team productivity.",
        "Marketing strategies are essential for startup growth.",
        "Investing in startups requires careful risk management.",
        "Financial planning is key for business sustainability.",
        "Entrepreneurship requires passion and perseverance.",
        "Understanding customer needs is vital for any business.",
        "Networking can create significant opportunities for growth.",
        "Management skills help maintain efficient operations."
    ],
    "Design": [
        "UI/UX design enhances user engagement and satisfaction.",
        "Typography choices can make or break a design.",
        "Branding creates a lasting impression on customers.",
        "Graphic design tools like Photoshop and Illustrator are widely used.",
        "Animation adds life to visual storytelling.",
        "Illustration can convey complex ideas visually.",
        "Color theory is fundamental for appealing designs.",
        "Product design should focus on usability and aesthetics."
    ],
    "Lifestyle": [
        "Maintaining a healthy diet is crucial for wellness.",
        "Traveling exposes you to new cultures and experiences.",
        "Fitness routines can improve both body and mind.",
        "Mindfulness and meditation help reduce stress.",
        "Photography captures life's memorable moments.",
        "Exploring hobbies enriches your personal life.",
        "Fashion trends reflect individuality and creativity.",
        "Wellness practices improve overall quality of life."
    ]
}

with app.app_context():
    # --- Clear existing data ---
    db.session.query(Comment).delete()
    db.session.query(Post).delete()
    db.session.query(Tag).delete()
    db.session.query(Category).delete()
    db.session.query(User).delete()
    db.session.commit()

    # --- Seed Users ---
    users = []
    user_credentials = []  # store plain password for login
    for _ in range(10):
        password = "Password123"  # simple password for testing
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        users.append(user)
        user_credentials.append((user.username, password))
    db.session.commit()

    print("✅ Seeded users with credentials (username : password):")
    for username, password in user_credentials:
        print(f"{username} : {password}")

    # --- Seed Categories & Tags ---
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

    # --- Seed Posts ---
    posts = []
    for _ in range(20):
        user_obj = fake.random_element(users)
        category = fake.random_element(categories)

        # 2–3 paragraphs per post
        paragraphs = []
        for _ in range(fake.random_int(min=2, max=3)):
            sentences = fake.random_elements(
                elements=category_sentences[category.name],
                length=fake.random_int(min=5, max=8),
                unique=True
            )
            paragraphs.append(" ".join(sentences))

        # Add headings to some paragraphs for realism
        content_paragraph = "\n\n".join(
            f"### {fake.sentence(nb_words=4)}\n\n{p}" if fake.boolean(50) else p
            for p in paragraphs
        )

        # Meaningful excerpt
        excerpt_text = " ".join(content_paragraph.split()[:50]) + "..."

        # Reliable featured image
        featured_image = f"https://picsum.photos/seed/{fake.uuid4()}/800/600"

        post = Post(
            title=fake.sentence(nb_words=8),
            content=content_paragraph,
            excerpt=excerpt_text,
            featured_image=featured_image,
            published=fake.boolean(chance_of_getting_true=70),
            user_id=user_obj.id,
            category_id=category.id
        )
        db.session.add(post)
        posts.append(post)
    db.session.commit()

    # Assign random tags from post's category
    for post in posts:
        category_tags = [tag for tag in tags if tag.category_id == post.category_id]
        post.tags = fake.random_elements(
            elements=category_tags,
            length=fake.random_int(min=1, max=4),
            unique=True
        )
    db.session.commit()

    # --- Seed Comments ---
    for _ in range(50):
        user_obj = fake.random_element(users)
        post = fake.random_element(posts)
        comment = Comment(
            content=fake.paragraph(nb_sentences=2),
            user_id=user_obj.id,
            post_id=post.id
        )
        db.session.add(comment)
    db.session.commit()

    print(f"✅ Seeded {len(users)} users, {len(categories)} categories, {len(tags)} tags, {len(posts)} posts, and 50 comments.")