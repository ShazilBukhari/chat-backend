from flask import Flask,jsonify,request
from flask_cors import CORS
from flask_jwt_extended import JWTManager,create_access_token,get_jwt_identity,jwt_required
from flask_socketio import SocketIO,join_room,emit
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)
socketio = SocketIO(app,cors_allowed_origins="*")

def get_connect():
  return sqlite3.connect(os.getenv("DATABASE_URL"))

def create_table():
  conn = get_connect()
  conn.execute("""CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               phonenumber TEXT NOT NULL,
               password TEXT NOT NULL
               )""")
  conn.execute("""CREATE TABLE IF NOT EXISTS messages(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               sender_id INTEGER NOT NULL,
               receiver_id INTEGER NOT NULL,
               message TEXT NOT NULL,
               timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               )""")
  conn.commit()
  conn.close()

create_table()

@app.route("/api/signup",methods=["POST"])
def signup():
  data = request.get_json()
  username = data.get("username")
  phone_number = data.get("phonenumber")
  password = data.get("password")
  if not username or not phone_number or not password:
    return jsonify({"error":"All Fields Are Mandatory"}),400
  hash_password = generate_password_hash(password)
  conn = get_connect()
  cursor = conn.execute("SELECT username FROM users WHERE username = ?",(username,))
  exist = conn.execute("SELECT phonenumber FROM users WHERE phonenumber = ?",(phone_number,)).fetchone()
  user = cursor.fetchone()
  if user:
    conn.close()
    return jsonify({"error":"Username already exits"}),400
  if exist:
    conn.close()
    return jsonify({"error":"Phone Number already exits"}),400
  conn.execute("INSERT INTO users(username,phonenumber,password) VALUES(?,?,?)",(username,phone_number,hash_password))
  conn.commit()
  conn.close()
  return jsonify({"message":"User Registered Successfully"}),201

@app.route("/api/login",methods=["POST"])
def login():
  data = request.get_json()
  username = data.get("username")
  password = data.get("password")
  if not username or not password:
    return jsonify({"error":"All Fields Are Mandatory"}),400
  conn = get_connect()
  cursor = conn.execute("SELECT id,password FROM users WHERE username = ?",(username,))
  user = cursor.fetchone()
  if not user:
    conn.close()
    return jsonify({"error":"User Not Found"}),401
  if not check_password_hash(user[1],password):
    conn.close()
    return jsonify({"error":"Invalid Password"}),401
  
  access_token = create_access_token(identity=str(user[0]))
  
  return jsonify({"message":"Login Successfully","access_token":access_token}),201

@app.route("/api/chat",methods=["GET"])
@jwt_required()
def chat():
  current_user = get_jwt_identity()
  return jsonify({"id":current_user,"message":"Acess Granted"}),201

@app.route("/api/users",methods=["GET"])
@jwt_required()
def sidebar_users():
  current_user = get_jwt_identity()
  conn = get_connect()
  cursor = conn.execute("SELECT id,username FROM users WHERE id != ?",(current_user,))
  user = cursor.fetchall()
  conn.close()
  users_list = []
  for u in user:
    users_list.append({
      "id":u[0],
      "username":u[1]
    })
  
  return jsonify(users_list),200

@app.route("/api/messages/<int:receiver_id>",methods=["GET"])
@jwt_required()
def chat_history(receiver_id):
  current_user = get_jwt_identity()
  conn = get_connect()
  cursor = conn.execute("SELECT sender_id,message,timestamp FROM messages WHERE (sender_id=? AND receiver_id=?) OR (sender_id=? AND receiver_id=?) ORDER BY timestamp ASC",(current_user,receiver_id,receiver_id,current_user))
  message_fetch = cursor.fetchall()
  conn.close()

  message_list = []
  for msg in message_fetch:
    message_list.append({
      "sender_id":msg[0],
      "message":msg[1],
      "timestamp":msg[2]
    })

  return jsonify(message_list),200

@socketio.on("user-connected")
def user_con():
  print("User Connected")

@socketio.on("join")
def join_users(data):
  user_id = data.get("user_id")
  if user_id:
    join_room(str(user_id))
    print(f"User {user_id} joined their private room")

@socketio.on("send-message")
def handle_message(data):
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  sender_id = data.get("sender_id")
  receiver_id = data.get("receiver_id")
  message = data.get("message")

  if sender_id and receiver_id and message:
    conn = get_connect()
    conn.execute("INSERT INTO messages(username,sender_id, receiver_id, message,timestamp) VALUES(?,?,?,?,?)",("N/A",sender_id,receiver_id,message,current_time))
    conn.commit()
    conn.close()
    socketio.emit("receive-message",{
      'sender_id':sender_id,
      'receiver_id':receiver_id,
      'message':message,
      'timestamp': current_time
    },room=str(receiver_id))

if __name__ == "__main__":
  socketio.run(app,debug=True)