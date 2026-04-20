from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
import sqlite3
import hashlib

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# SQLite init
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        return jsonify({"message": "user created"})
    except:
        return jsonify({"error": "username exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password_hash))
    user = cursor.fetchone()
    
    if user:
        token = create_access_token(identity=username)
        return jsonify({"token": token})
    return jsonify({"error": "invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True)
