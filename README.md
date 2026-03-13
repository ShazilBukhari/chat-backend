# 💬 Real-Time Chat Application (Flask + Socket.IO)

A secure real-time chat backend built using Flask, JWT authentication, and Socket.IO.  
This project supports user authentication, private messaging, and live communication.

---

## 🚀 Features

- User Signup & Login
- JWT Authentication
- Real-time Private Messaging
- Fetch All Users (except logged-in user)
- Chat History between users
- SQLite Database
- Password Hashing (Werkzeug)
- CORS Enabled
- Private Rooms for secure messaging

---

## 🛠 Tech Stack

- Flask
- Flask-JWT-Extended
- Flask-SocketIO
- Flask-CORS
- SQLite
- Werkzeug Security
- Python Dotenv

---

## 📁 Project Structure


app.py
.env
database.db
README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Project

git clone <your-repo-link>
cd <project-folder>


### 2️⃣ Create Virtual Environment

python -m venv venv


Activate:

**Windows**

venv\Scripts\activate


**Mac/Linux**

source venv/bin/activate


### 3️⃣ Install Dependencies

pip install flask flask-cors flask-jwt-extended flask-socketio python-dotenv werkzeug


### 4️⃣ Create `.env` File


JWT_SECRET_KEY=your_secret_key
DATABASE_URL=database.db


### 5️⃣ Run the App

python app.py


Server will run at:

http://localhost:5000


---

## 🔌 API Endpoints

### 🔐 Authentication

#### Signup
POST `/api/signup`

Body:

{
"username": "john",
"phonenumber": "1234567890",
"password": "password123"
}


---

#### Login
POST `/api/login`

Body:

{
"username": "john",
"password": "password123"
}


Response:

{
"message": "Login Successfully",
"access_token": "JWT_TOKEN"
}


---

## 🔒 Protected Routes

Add this header:

Authorization: Bearer <your_token>


### Get All Users
GET `/api/users`

### Get Chat History
GET `/api/messages/<receiver_id>`

### Test Route
GET `/api/chat`

---

## 🔥 Socket.IO Events

### Connect

user-connected


### Join Room

join


Data:

{
"user_id": "1"
}


### Send Message

send-message


Data:

{
"sender_id": "1",
"receiver_id": "2",
"message": "Hello!"
}


### Receive Message

receive-message


---

## 🗄 Database Tables

### Users Table
- id
- username
- phonenumber
- password

### Messages Table
- id
- username
- sender_id
- receiver_id
- message
- timestamp

---

## 🔐 Security

- Password hashing
- JWT authentication
- Protected APIs
- Private socket rooms
- Environment variables for secrets

---

## 🎯 Future Improvements

- Online/Offline Status
- Message Seen Status
- Group Chats
- Profile Pictures
- Deployment (Render / Railway / VPS)
- Frontend Integration (React)

---

## 👨‍💻 Author

Built with ❤️ using Flask & Socket.IO.

---

## 📜 License

Open-source project.
