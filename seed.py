import random
from models import db, User, Post, Comment, Category, Tag, Reply
from app import app
from werkzeug.security import generate_password_hash

# --- Kenyan Users ---
kenyan_users = [
    {"username": "wanjiku_m", "email": "wanjiku.mwangi@gmail.com"},
    {"username": "otieno_k", "email": "kevin.otieno@gmail.com"},
    {"username": "akinyi_a", "email": "akinyi.adhiambo@gmail.com"},
    {"username": "kamau_j", "email": "james.kamau@gmail.com"},
    {"username": "njeri_w", "email": "njeri.wambui@gmail.com"},
    {"username": "odhiambo_b", "email": "brian.odhiambo@gmail.com"},
    {"username": "chebet_r", "email": "ruth.chebet@gmail.com"},
    {"username": "mutua_d", "email": "david.mutua@gmail.com"},
    {"username": "wairimu_g", "email": "grace.wairimu@gmail.com"},
    {"username": "kipchoge_e", "email": "elijah.kipchoge@gmail.com"},
]

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

# --- Kenyan-context posts ---
posts_data = [
    {
        "category": "Technology",
        "title": "How Kenyan Developers Are Shaping Africa's Tech Future",
        "excerpt": "From Nairobi's Silicon Savannah to global stages, Kenyan developers are building solutions that matter.",
        "content": """### The Rise of Silicon Savannah\n\nNairobi has earned its nickname as Africa's Silicon Savannah. With hubs like iHub and Nairobi Garage, local developers are building world-class products. Companies like Andela and Safaricom's M-Pesa have put Kenya on the global tech map.\n\n### Why Kenya Leads in Fintech\n\nM-Pesa revolutionized mobile money not just in Kenya but across the world. Today, startups like Pezesha and Lipa Later are continuing that legacy by making financial services accessible to millions of unbanked Kenyans. The ecosystem is thriving and attracting global investors.\n\n### What's Next\n\nWith 5G rollout underway and a young, tech-savvy population, Kenya is poised to lead the next wave of African innovation. From agritech to healthtech, Kenyan developers are solving real problems with elegant solutions.""",
        "tags": ["Web Development", "AI", "DevOps"]
    },
    {
        "category": "Technology",
        "title": "Building Your First React App: A Guide for Kenyan Developers",
        "excerpt": "A practical guide to getting started with React, tailored for developers in Kenya.",
        "content": """### Getting Started with React\n\nReact is one of the most in-demand skills in Kenya's job market today. Whether you're applying at a Nairobi startup or freelancing on Upwork, knowing React opens doors. This guide walks you through setting up your first project.\n\n### Setting Up Your Environment\n\nFirst, install Node.js from nodejs.org. Then run `npx create-react-app my-app` in your terminal. Within minutes you'll have a working React application. Tools like VS Code, which is free, make development smooth even on lower-spec machines common in Kenya.\n\n### Building Something Useful\n\nInstead of a generic todo app, try building something relevant — a matatu route finder, a local market price tracker, or a community notice board. Real projects teach you faster and make your portfolio stand out to Kenyan employers.""",
        "tags": ["React", "JavaScript", "Web Development"]
    },
    {
        "category": "Technology",
        "title": "Cybersecurity in Kenya: Protecting Your Digital Life",
        "excerpt": "As internet usage grows in Kenya, so do cyber threats. Here's how to stay safe online.",
        "content": """### The Growing Threat Landscape\n\nKenya recorded over 860 million cyber threats in 2023 according to the Communications Authority. From phishing emails targeting M-Pesa users to ransomware hitting businesses, the threats are real and growing. Awareness is your first line of defense.\n\n### Common Scams Targeting Kenyans\n\nSIM swap fraud is rampant — attackers convince Safaricom or Airtel to transfer your number to their SIM, then drain your M-Pesa. Always use a strong PIN and enable two-factor authentication on all accounts. Be wary of calls claiming to be from your bank or mobile provider.\n\n### How to Stay Safe\n\nUse strong, unique passwords for every account. Enable 2FA wherever possible. Keep your phone's OS updated. Avoid public Wi-Fi for banking. Report suspicious activity to your bank immediately. Kenya's Computer Misuse and Cybercrimes Act 2018 provides legal recourse for victims.""",
        "tags": ["Cybersecurity", "DevOps"]
    },
    {
        "category": "Business",
        "title": "Starting a Business in Kenya: What No One Tells You",
        "excerpt": "The real challenges and opportunities of entrepreneurship in Kenya, from registration to scaling.",
        "content": """### Registering Your Business\n\nRegistering a business in Kenya has become easier with the eCitizen portal. You can register a sole proprietorship for as little as Ksh 950 or a limited company for around Ksh 10,000. The process takes a few days if your documents are in order. Don't skip this step — operating informally limits your access to tenders and bank loans.\n\n### Funding Your Startup\n\nBootstrapping is the reality for most Kenyan entrepreneurs. But options exist — Youth Enterprise Development Fund, Women Enterprise Fund, and Uwezo Fund offer government-backed loans. Angel investors and VCs like Savannah Fund and DOB Equity are actively looking for Kenyan startups with traction.\n\n### The Hustle is Real\n\nKenya's business environment is competitive. Load shedding, high internet costs, and bureaucracy are real challenges. But the market is large, the middle class is growing, and Kenyans are resilient. Focus on solving a real problem, keep your costs lean, and build genuine relationships.""",
        "tags": ["Startup", "Entrepreneurship", "Finance"]
    },
    {
        "category": "Business",
        "title": "How to Use Social Media Marketing to Grow Your Kenyan Business",
        "excerpt": "Practical social media strategies that work for small and medium businesses in Kenya.",
        "content": """### Where Kenyans Spend Their Time Online\n\nFacebook, Instagram, TikTok, and X (Twitter) are the dominant platforms in Kenya. WhatsApp is king for direct customer communication. Understanding where your target audience is helps you focus your energy and budget effectively.\n\n### Content That Resonates\n\nKenyans respond well to authentic, relatable content. Use Swahili and Sheng where appropriate — it builds trust and connection. Behind-the-scenes content, customer testimonials, and educational posts perform well. Avoid overly polished corporate content; it feels distant.\n\n### Paid Advertising on a Budget\n\nFacebook and Instagram ads can be run for as little as Ksh 500 per day. Target by location, age, and interests. Start small, test different creatives, and scale what works. Many Nairobi businesses have grown significantly through consistent, targeted social media advertising.""",
        "tags": ["Marketing", "Strategy", "Startup"]
    },
    {
        "category": "Business",
        "title": "Investing in Kenya: From Chamas to the Nairobi Stock Exchange",
        "excerpt": "A beginner's guide to growing your wealth through Kenya's diverse investment options.",
        "content": """### The Power of Chamas\n\nChamas — informal investment groups — are a uniquely Kenyan institution. They pool resources, invest collectively, and have funded everything from rental properties to businesses. A well-run chama with clear rules and accountability can be one of the best investment vehicles available.\n\n### NSE and Unit Trusts\n\nThe Nairobi Securities Exchange lists over 60 companies. You can start investing with as little as Ksh 1,000 through a licensed stockbroker. Unit trusts like those offered by CIC, Britam, and Sanlam allow even smaller investments with professional management.\n\n### Real Estate and REITs\n\nReal estate has traditionally been the preferred investment for Kenyans. With REITs now available on the NSE, you can invest in property without buying land. Platforms like Acorn Holdings' REIT make it accessible to everyday investors. Diversify — don't put all your eggs in one basket.""",
        "tags": ["Investing", "Finance", "Economics"]
    },
    {
        "category": "Design",
        "title": "UI/UX Design for African Users: Lessons from Kenya",
        "excerpt": "Designing digital products for Kenyan users requires understanding local context, constraints, and culture.",
        "content": """### Design for Low Bandwidth\n\nMany Kenyan users access the internet on mobile data, often on 3G networks. Heavy images, autoplay videos, and bloated JavaScript kill the experience. Design with performance in mind — compress images, lazy load content, and test on mid-range Android devices, not just the latest iPhone.\n\n### Language and Localization\n\nEnglish and Swahili are both widely used. Consider offering your interface in both languages. Use familiar local references — M-Pesa for payments, county names for location, Kenyan phone number formats. Small localization details build enormous trust with users.\n\n### Color and Cultural Context\n\nColors carry meaning. Green is associated with money and growth in Kenya. Red can signal danger or urgency. Research your specific audience — a product for Maasai communities may have different color associations than one for urban Nairobi youth. Always test with real users from your target market.""",
        "tags": ["UI/UX", "Product Design", "Branding"]
    },
    {
        "category": "Design",
        "title": "Building a Personal Brand as a Creative in Nairobi",
        "excerpt": "How Nairobi's creatives are standing out in a crowded market through intentional personal branding.",
        "content": """### Why Personal Branding Matters\n\nNairobi's creative scene is vibrant and competitive. Graphic designers, photographers, illustrators, and animators are everywhere. What sets the successful ones apart is not just skill — it's how they present themselves. A strong personal brand makes you memorable and commands better rates.\n\n### Building Your Online Presence\n\nStart with a clean portfolio website. Behance and Dribbble are great for designers. Instagram works well for visual creatives. Post consistently, show your process, not just final results. Clients want to see how you think, not just what you produce.\n\n### Networking in Nairobi\n\nAttend events like Nairobi Design Week, creative meetups at spaces like The Alchemist, and industry conferences. Nairobi's creative community is tight-knit and supportive. Collaborations often lead to referrals. Be genuine, be helpful, and your reputation will grow organically.""",
        "tags": ["Branding", "Visual Identity", "Graphic Design"]
    },
    {
        "category": "Lifestyle",
        "title": "The Best Weekend Getaways from Nairobi",
        "excerpt": "You don't need to travel far to recharge. Kenya's best escapes are just hours from Nairobi.",
        "content": """### Naivasha: Nature at Its Best\n\nLake Naivasha is just 90 minutes from Nairobi and offers boat rides, hippo spotting, and cycling through Hell's Gate National Park. Accommodation ranges from budget campsites to luxury lodges. It's the perfect quick escape for nature lovers and families alike.\n\n### Nanyuki and Mount Kenya\n\nFor the adventurous, Nanyuki is the gateway to Mount Kenya. Even if you're not climbing, the area offers stunning scenery, wildlife conservancies, and excellent food. The drive through Thika and Karatina is scenic and the air is refreshingly cool compared to Nairobi.\n\n### The Coast: Mombasa and Beyond\n\nA weekend at the coast requires a flight or overnight bus, but it's worth it. Diani Beach consistently ranks among Africa's best beaches. Watamu and Malindi offer a quieter, more authentic experience. The Swahili culture, fresh seafood, and warm Indian Ocean make the coast a perennial favourite for Nairobians.""",
        "tags": ["Travel", "Hobbies", "Wellness"]
    },
    {
        "category": "Lifestyle",
        "title": "Eating Well in Nairobi: A Guide to Local and Healthy Food",
        "excerpt": "From nyama choma joints to health-conscious cafes, Nairobi's food scene has something for everyone.",
        "content": """### Traditional Kenyan Foods Worth Embracing\n\nUgali, sukuma wiki, githeri, and mukimo are not just traditional — they're nutritious and affordable. Sukuma wiki (kale) is rich in iron and vitamins. Githeri (maize and beans) is a complete protein. These foods have sustained Kenyans for generations and deserve more respect than they get.\n\n### Nairobi's Growing Health Food Scene\n\nRestaurants like Cultiva, Harvest, and various spots in Westlands and Karen now offer organic, locally sourced meals. Farmers markets in Lavington and Gigiri sell fresh produce directly from farms. Eating local reduces your carbon footprint and supports Kenyan farmers.\n\n### Staying Fit on a Budget\n\nYou don't need an expensive gym membership to stay fit in Nairobi. Karura Forest offers free walking and cycling trails. Uhuru Park and City Park are accessible green spaces. Many estates have football pitches and outdoor gyms. Consistency matters more than the facility.""",
        "tags": ["Food", "Health", "Fitness"]
    },
    {
        "category": "Technology",
        "title": "Python for Data Science: Opportunities for Kenyan Analysts",
        "excerpt": "Data science skills are in high demand across Kenya's banking, telecom, and government sectors.",
        "content": """### Why Data Science in Kenya Now\n\nKenya's banking sector, telecoms like Safaricom, and government agencies are sitting on massive datasets. The demand for analysts who can extract insights is growing faster than the supply of skilled professionals. Python is the tool of choice for most data science work globally and in Kenya.\n\n### Getting Started with Python\n\nPython is free and beginner-friendly. Start with the basics — variables, loops, functions. Then move to pandas for data manipulation and matplotlib for visualization. Free resources like Kaggle, Coursera, and YouTube channels make learning accessible even without formal education.\n\n### Real Kenyan Use Cases\n\nAnalyzing M-Pesa transaction patterns to detect fraud. Predicting crop yields for smallholder farmers. Mapping disease outbreaks for the Ministry of Health. These are real problems being solved with Python and data science right now in Kenya. The opportunities are enormous for those willing to learn.""",
        "tags": ["Python", "Data Science", "Machine Learning"]
    },
    {
        "category": "Business",
        "title": "Remote Work in Kenya: How to Land International Clients",
        "excerpt": "Kenyan freelancers are earning in dollars and euros. Here's how to position yourself for global opportunities.",
        "content": """### Platforms That Work for Kenyans\n\nUpwork, Fiverr, Toptal, and Contra are all accessible from Kenya. M-Pesa and Payoneer make receiving international payments straightforward. The key is building a strong profile with clear positioning — don't try to do everything, specialize in one or two skills.\n\n### Building Credibility from Scratch\n\nStart by doing a few projects at lower rates to build reviews and a portfolio. Reach out to diaspora Kenyans running businesses abroad — they often prefer working with people from home. LinkedIn is underutilized by Kenyan freelancers but is extremely effective for B2B services.\n\n### Managing Time Zones and Communication\n\nWorking with clients in the US or Europe means odd hours sometimes. Be upfront about your availability. Over-communicate — send updates before clients ask. Reliability and clear communication are what turn one-off clients into long-term relationships. Many Kenyan freelancers now earn more than local corporate salaries.""",
        "tags": ["Productivity", "Strategy", "Entrepreneurship"]
    },
]

# --- Kenyan-context comments ---
comments_data = {
    "Technology": [
        "Hii ni ukweli kabisa! Nairobi tech scene inakua haraka sana. Nimejaribu kuapply kwa Andela na ilikuwa competitive sana.",
        "Great article! As a developer in Kisumu, I feel like we're often left out of the conversation. Would love to see more content about tech outside Nairobi.",
        "M-Pesa changed everything for us. My whole business runs on it. Kudos to Safaricom for that innovation.",
        "React imekuwa game changer kwangu. Nilianza kujifunza mwaka jana na sasa ninapata freelance work. Asante kwa guide hii.",
        "Cybersecurity is so important. My cousin lost Ksh 50,000 to a SIM swap last year. People need to know about this.",
        "Python ndio lugha ninayopenda zaidi. Data science opportunities in Kenya are real — I work at a bank and we use it daily.",
        "This is exactly what I needed. Starting my React journey this week. Nairobi tech community is very supportive.",
        "The Silicon Savannah narrative is inspiring but we need more infrastructure support from the government.",
    ],
    "Business": [
        "Nilijaribu kuregister biashara yangu na eCitizen ilikuwa rahisi kuliko nilivyofikiri. Took less than a week!",
        "Chamas are underrated investment vehicles. Our chama has been running for 8 years and we now own two rental properties in Ruiru.",
        "Social media marketing imesaidia sana biashara yangu ya mitumba. Instagram especially works well for fashion.",
        "The NSE is something more young Kenyans should explore. I started with Ksh 5,000 and have been learning a lot.",
        "Remote work changed my life. I now earn in USD while living in Nakuru. The cost of living difference is massive.",
        "Starting a business in Kenya is tough but possible. The bureaucracy is real but don't let it stop you.",
        "Uwezo Fund helped me start my small business in Eldoret. Government funding programs are worth exploring.",
        "LinkedIn is so underused by Kenyans. I got my best client through LinkedIn after just 3 months of consistent posting.",
    ],
    "Design": [
        "Designing for low bandwidth is something I wish more Kenyan developers thought about. My mum in the village struggles with heavy websites.",
        "Nairobi Design Week is amazing! Met so many talented creatives there last year. The community is very welcoming.",
        "Personal branding changed my career. I went from charging Ksh 5,000 per logo to Ksh 50,000 after building my portfolio properly.",
        "UI/UX for African users is such an important topic. We can't just copy Western design patterns and expect them to work here.",
        "The Alchemist events are great for networking. Nairobi's creative scene is world class, we just need to believe in ourselves.",
        "Localization is key. I always include Swahili options in my apps and users appreciate it so much.",
    ],
    "Lifestyle": [
        "Hell's Gate ni amazing! Went last month with my family. The cycling is so much fun and very affordable.",
        "Diani Beach is paradise. Went for my honeymoon and we're already planning to go back. Kenya's coast is underrated globally.",
        "Sukuma wiki na ugali ndio staple yangu. Healthy, cheap, and delicious. Watu wanashindwa kwa nini wanakimbia traditional food.",
        "Karura Forest is my weekend therapy. Free entry, beautiful trails, and you forget you're in the middle of a city.",
        "Nairobi food scene imekua sana. The variety now is incredible — from nyama choma to sushi, all within a few kilometers.",
        "Nanyuki trip was one of the best decisions I made this year. Mount Kenya views are breathtaking.",
        "Eating local and seasonal is both healthy and supports our farmers. More Kenyans should embrace this.",
        "Watamu is so much better than Mombasa for a quiet beach holiday. Less crowded and more authentic.",
    ]
}

# --- Kenyan-context replies ---
replies_data = [
    "Nakubaliana nawe kabisa! Same experience hapa.",
    "Thanks for sharing this, very helpful for those of us just starting out.",
    "Hii ni kweli. Nimepitia hali kama hiyo pia.",
    "Great point! More people need to hear this.",
    "Asante sana kwa hii information. Itanisaidia sana.",
    "Exactly my thoughts! Glad someone said it.",
    "Nimejaribu hii na inafanya kazi. Highly recommend.",
    "This is so relatable. Nairobi life is something else!",
    "Pole kwa experience mbaya. Hope things are better now.",
    "Sawa kabisa. Keep pushing, success inakuja.",
    "I shared this with my chama group. Very relevant discussion.",
    "Wewe ni mtu wa busara. Good advice for all of us.",
]

with app.app_context():
    # --- Clear existing data ---
    db.session.query(Reply).delete()
    db.session.query(Comment).delete()
    db.session.execute(db.text('DELETE FROM post_tags'))
    db.session.query(Post).delete()
    db.session.query(Tag).delete()
    db.session.query(Category).delete()
    db.session.query(User).delete()
    db.session.commit()

    # --- Seed Users ---
    users = []
    for u in kenyan_users:
        user = User(username=u["username"], email=u["email"],
                    password_hash=generate_password_hash("Password123"))
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # --- Seed Categories & Tags ---
    categories = {}
    tags = []
    for cat_name, tag_list in categories_data.items():
        category = Category(name=cat_name)
        db.session.add(category)
        db.session.commit()
        categories[cat_name] = category
        for tag_name in tag_list:
            tag = Tag(name=tag_name, category_id=category.id)
            db.session.add(tag)
            tags.append(tag)
    db.session.commit()

    # --- Seed Posts ---
    posts = []
    image_ids = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    for i, p in enumerate(posts_data):
        category = categories[p["category"]]
        post_tags_objs = list({t.id: t for t in tags if t.name in p["tags"]}.values())
        post = Post(
            title=p["title"],
            content=p["content"],
            excerpt=p["excerpt"],
            featured_image=f"https://picsum.photos/seed/{image_ids[i % len(image_ids)]}/800/600",
            published=True,
            user_id=random.choice(users).id,
            category_id=category.id,
            tags=post_tags_objs
        )
        db.session.add(post)
        posts.append(post)
    db.session.commit()

    # --- Seed Comments ---
    comments = []
    for post in posts:
        cat_name = post.category.name
        pool = comments_data.get(cat_name, comments_data["Technology"])
        for content in random.sample(pool, min(3, len(pool))):
            comment = Comment(
                content=content,
                user_id=random.choice(users).id,
                post_id=post.id
            )
            db.session.add(comment)
            comments.append(comment)
    db.session.commit()

    # --- Seed Replies ---
    for comment in comments:
        for reply_content in random.sample(replies_data, random.randint(1, 3)):
            reply = Reply(
                content=reply_content,
                user_id=random.choice(users).id,
                comment_id=comment.id
            )
            db.session.add(reply)
    db.session.commit()

    print(f"✅ Seeded {len(users)} users, {len(categories)} categories, {len(tags)} tags, {len(posts)} posts, {len(comments)} comments, and replies.")
    print("\n📋 Login credentials (all users):")
    for u in kenyan_users:
        print(f"  {u['username']} : Password123")
