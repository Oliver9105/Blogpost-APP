# Blogpost-APP

A web application designed to help users create, view, and comment on blog posts. Built using React for the frontend and Flask for the backend.

## By Oliver (Oliver9105)

### Description

Blog Post App is a full-stack application that demonstrates core React concepts including components, state management, and routing with React Router. On the backend, it uses Flask to provide a RESTful API. Users can register, create posts, view posts, and add comments. This project serves as a learning tool for mastering full-stack web development.

---

## 🚀 Features

- Home page displaying a list of blog posts.
- User profile creation and management.
- Post creation and management.
- Commenting on posts.
- Responsive and clean UI design.

---

## 📝 How to Use

### Requirements

- A computer, tablet, or phone.
- Access to the internet.
- A modern web browser.

### View Live Site

Visit the deployed application at: [oliver-blogspace.netlify.app](https://oliver-blogspace.netlify.app)

The live site allows you to:

- Browse and create profiles.
- Create and view blog posts.
- Add and view comments.

### 💻 Local Development

If you want to run the project locally, you'll need:

- Python and Flask installed on your computer.
- Basic understanding of React and Flask.
- Code editor (VS Code recommended).
- Terminal/Command Line.

#### 📥 Installation Process

1. Clone the repositories:

   ```bash
   git clone git@github.com:Oliver9105/Blogpost-APP.git  f
   git clone git@github.com:Oliver9105/Blogpost_client.git
   ```

2. Navigate to the backend directory and install dependencies:

   ```bash
   cd Blogpost-APP
   pip install -r requirements.txt
   ```

   download and install environment shell dependencies and create environment

   ```
   pipenv install && pipenv shell
   ```

3. Start the backend server:

   ```bash
   flask run
   # or
   python app.py
   ```

4. Navigate to the frontend directory and install dependencies:
   ```bash
   cd Blogpost_client
   npm install
   ```
5. Start the frontend development server:

   ```bash
   npm start
   ```

6. Open your browser and visit [http://localhost:3000](http://localhost:3000)

---

## ⚙️ Backend

The backend of this application is built using Flask, with Flask-SQLAlchemy for interacting with the database. The database models include User, Post, and Comment, which are linked through one-to-many relationships. Passwords are securely hashed using Werkzeug for authentication. The app follows a RESTful API design using Flask-RESTful to handle CRUD operations for users, posts, and comments. Additionally, SQLAlchemy Serializer is used to convert models to JSON and implement model validation to ensure data integrity.

### Backend Features

- **User Management:** Register and authenticate users with secure password hashing.
- **Post Management:** Create, read, update, and delete posts.
- **Comment Management:** Add, view, and delete comments on posts.
- **Database Models:** User, Post, Comment with one-to-many relationships.
- **Validation:** Ensures data integrity with model validation.
- **Serialization:** Converts models to JSON for API responses.

**Backend Repository:** [Blogpost-APP](https://github.com/Oliver9105/Blogpost-APP.git)  
**Deployed API:** [https://blogpost-app-qx9s.onrender.com](https://blogpost-app-qx9s.onrender.com)

---

## 🌐 Frontend

The frontend of this application is built with React. It allows users to interact with the application by viewing posts, creating new posts, and adding comments. The frontend is deployed on Netlify.

### Frontend Features

- **Home Page:** Displays a list of posts with links to view individual posts.
- **View Post Page:** Displays the details of a single post along with its comments and a form to add new comments.
- **Create Post Page:** Provides a form to create a new post.
- **Authors Page:** Displays a list of authors.

**Frontend Repository:** [Blogpost_client](https://github.com/Oliver9105/Blogpost_client.git)  
**Deployed Frontend:** [oliver-blogspace.netlify.app](https://oliver-blogspace.netlify.app)

---

## 🗃️ API Endpoints

### Users

- **POST /users:** Create a new user
  ```json
  {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "password123"
  }
  ```

### Posts

- **GET /posts:** Get all posts
- **GET /posts/:id:** Get a post by ID
- **POST /posts:** Create a new post
  ```json
  {
    "title": "My First Post",
    "content": "This is the content of my first post",
    "user_id": 1
  }
  ```

### Comments

- **GET /posts/:id/comments:** Get comments for a post
- **POST /posts/:id/comments:** Add a comment to a post
  ```json
  {
    "user_id": 1,
    "content": "This is a comment"
  }
  ```

---

## 🛠️ Technologies Used

- **React** - JavaScript library for building user interfaces.
- **React Router** - Library for routing in React applications.
- **Formik** - Library for building and managing forms.
- **Yup** - Library for form validation.
- **Flask** - Python micro-framework for the backend.
- **CSS3** - Styling.
- **JavaScript (ES6)** - Scripting language.
- **Python** - Programming language.
- **Netlify** - Platform for deploying the frontend.

---

## 🤝 Support and Contact Details

If you have any questions, suggestions, or need assistance, please contact:

- 📧 **Email:** [Olivercher1000@gmail.com](mailto:Olivercher1000@gmail.com)

---

## 📜 License

MIT License © 2025 Oliver (Oliver9105)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.** IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
