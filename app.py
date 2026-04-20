from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    if username == 'admin' and password == '1234':
        return jsonify({"token": "jwt_token_here", "status": "success"})
    return jsonify({"error": "invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True)
