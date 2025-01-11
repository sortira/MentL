from mail import sendmail 
import os
from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
import jinja2
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import secrets
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = secrets.token_hex(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id, password=None):
        self.id = id
        self.password = password

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user_ref = db.collection('users').document(email)
    if user_ref.get().exists:
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    user_ref.set({
        'email': email,
        'password': hashed_password
    })
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user_ref = db.collection('users').document(email)
    user_doc = user_ref.get()
    if not user_doc.exists:
        return jsonify({'error': 'Invalid email or password'}), 401

    user_data = user_doc.to_dict()
    if not check_password_hash(user_data['password'], password):
        return jsonify({'error': 'Invalid email or password'}), 401

    user = User(email)
    login_user(user)
    return jsonify({'message': 'Logged in successfully'}), 200

@app.route('/')
def home():
    return render_template('home.html')

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User(email)
    return user

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

@app.route('/sleep', methods=['POST'])
@login_required
def log_sleep():
    data = request.get_json()
    hours = data.get('hours')
    date = data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))

    if not hours:
        return jsonify({'error': 'Hours slept is required'}), 400

    db.collection('users').document(current_user.id).collection('sleep').document(date).set({
        'hours': hours,
        'date': date
    })
    return jsonify({'message': 'Sleep data recorded successfully'}), 201

@app.route('/physical_activity', methods=['POST'])
@login_required
def log_physical_activity():
    data = request.get_json()
    hours = data.get('hours')
    date = data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))

    if not hours:
        return jsonify({'error': 'Hours of physical activity is required'}), 400

    db.collection('users').document(current_user.id).collection('physical_activity').document(date).set({
        'hours': hours,
        'date': date
    })
    return jsonify({'message': 'Physical activity data recorded successfully'}), 201

@app.route('/food', methods=['POST'])
@login_required
def log_food():
    data = request.get_json()
    calories = data.get('calories')
    date = data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))

    if not calories:
        return jsonify({'error': 'Calories consumed is required'}), 400

    db.collection('users').document(current_user.id).collection('food').document(date).set({
        'calories': calories,
        'date': date
    })
    return jsonify({'message': 'Food data recorded successfully'}), 201

@app.route('/journalling', methods=['POST'])
@login_required
def log_journalling():
    data = request.get_json()
    content = data.get('content')
    date = data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))

    if not content:
        return jsonify({'error': 'Journal content is required'}), 400

    db.collection('users').document(current_user.id).collection('journals').document(date).set({
        'content': content,
        'date': date
    })
    return jsonify({'message': 'Journal recorded successfully'}), 201

@app.route('/<category>', methods=['GET'])
@login_required
def fetch_data(category):
    valid_categories = ['sleep', 'physical_activity', 'food', 'journals']

    if category not in valid_categories:
        return jsonify({'error': 'Invalid category'}), 400

    docs = db.collection('users').document(current_user.id).collection(category).stream()
    data = {doc.id: doc.to_dict() for doc in docs}

    return jsonify(data), 200


# ==================================================================================

@app.route('/login', methods=['GET'])
def send_login_page():
    return render_template('xxxlogin.html')
@app.route('/login_2', methods=['GET'])
def send_login_2_page():
    return render_template('login.html')


@app.route('/signup', methods=['GET'])
def send_signup_page():
    return render_template('xxxsignup.html')


if __name__ == '__main__':
    app.run(debug=True)
