from flask import Flask, render_template, redirect, request, session
import json

app = Flask(__name__)
app.secret_key = "c69a10a733124d160d031d2f75a6fa1244c6c9a11f4a63f4fbc2af5780166a10"  # Replace with your own secret key


@app.route('/')
def index():
    # Render the client login page
    return render_template('client_login.html')


@app.route('/redirect-to-oauth')
def redirect_to_oauth():
    # Redirect to the OAuth server
    return redirect('http://localhost:5000')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Perform your login authentication logic here
        # ...

        # Assuming authentication is successful, retrieve user info from JSON file
        with open('user_info.json', 'r') as f:
            user_info = json.load(f)
            if username in user_info and user_info[username]['password'] == password:
                # Store the username in the session and retrieve client_id and client_secret
                session['username'] = username
                client_id = user_info[username]['client_id']
                client_secret = user_info[username]['client_secret']

                # Redirect to the client index page with username, client_id, and client_secret as URL parameters
                return redirect('/client_index?username={}&client_id={}&client_secret={}'.format(username, client_id, client_secret))

        # If authentication fails, display an error message
        return "Invalid username or password."

    # Render the client login page
    return render_template('client_login.html')


@app.route('/client_index')
def client_index():
    # Retrieve username, client_id, and client_secret from the session and request URL parameters
    username = session.get('username')
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')

    # Render the client index page with username, client_id, and client_secret
    return render_template('client_index.html', username=username, client_id=client_id, client_secret=client_secret)


@app.route('/home')
def home():
    # Retrieve username, client_id, and client_secret from the session and request URL parameters
    username = session.get('username') or request.args.get('username')
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')

    # Render the client index page with username, client_id, and client_secret
    return render_template('client_index.html', username=username, client_id=client_id, client_secret=client_secret)


if __name__ == '__main__':
    # Run the Flask application on port 8000 in debug mode
    app.run(port=8000, debug=True)
