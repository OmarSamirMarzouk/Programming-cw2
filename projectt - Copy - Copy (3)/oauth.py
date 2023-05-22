from flask import Flask, render_template, request, redirect, session
import secrets
import jwt
import json
import os

app = Flask(__name__)
app.secret_key = "YourSecretKey"  # Replace with your own secret key

# In a real application, you would store the user information securely in a database
users = []
secret_key = "c69a10a733124d160d031d2f75a6fa1244c6c9a11f4a63f4fbc2af5780166a10"  # Replace with your own secret key
user_info_file = "user_info.json"  # JSON file to store user information


def save_user_info(users):
    with open("C:\\Users\\Omar\\Desktop\\projectt\\user_info.json", "w") as file:
        json.dump(users, file, indent=4)


def load_user_info():
    if os.path.exists(user_info_file):
        with open("C:\\Users\\Omar\\Desktop\\projectt\\user_info.json", "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_user_info()
        users.append({'username': username, 'password': password, 'client_id': None, 'client_secret': None})
        save_user_info(users)
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_user_info()
        for user in users:
            if user['username'] == username and user['password'] == password:
                client_id = user['client_id']
                client_secret = user['client_secret']
                if client_id is None or client_secret is None:
                    client_id = secrets.token_hex(16)
                    client_secret = secrets.token_hex(32)
                    user['client_id'] = client_id
                    user['client_secret'] = client_secret
                    save_user_info(users)

                # Create JWT token with user data
                payload = {
                    'username': username,
                    'client_id': client_id,
                    'client_secret': client_secret
                }
                token = jwt.encode(payload, secret_key, algorithm='HS256')

                # Save the token, client ID, and client secret in session
                session['token'] = token
                session['client_id'] = client_id
                session['client_secret'] = client_secret
                session['username'] = username  # Store the username in the session

                return redirect('/home')
        return "Invalid username or password."
    return render_template('login.html')


@app.route('/home')
def home():
    if 'token' in session and 'client_id' in session and 'client_secret' in session:
        token = session['token']
        client_id = session['client_id']
        client_secret = session['client_secret']

        # Retrieve the username from the session
        username = session.get('username')

        users = load_user_info()
        for user in users:
            if user['username'] == username and user['client_id'] == client_id and user['client_secret'] == client_secret:
                return render_template('home.html', username=username, client_id=client_id, client_secret=client_secret)

    return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect('/')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
