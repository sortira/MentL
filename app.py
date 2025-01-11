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

def calculate_sleep_score(email):
    try:
        user_ref = db.collection('users').document(email)
        user_data = user_ref.get()
        if not user_data.exists:
            print("User not found.")
            return None
        sleep_data = user_data.to_dict().get('sleep', [])
        if not sleep_data:
            print("No sleep data available.")
            return None
        total_sleep_hours = 0
        for entry in sleep_data:
            try:
                total_sleep_hours += float(entry.get('hours', 0))
            except ValueError:
                print(f"Invalid value for hours: {entry.get('hours')}, skipping this entry.")
                continue
        total_days = len(sleep_data)
        if total_days == 0:
            print("No days with sleep data.")
            return None
        sleep_score = (total_sleep_hours / (8 * total_days)) * 100
        if sleep_score > 100:
            sleep_score = 100
        return round(sleep_score, 2)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not email or not password or not name:
        return jsonify({'error': 'Email, name and password are required'}), 400

    user_ref = db.collection('users').document(email)
    if user_ref.get().exists:
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    user_ref.set({
        'email': email,
        'password': hashed_password,
        'name': name
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
    return redirect(url_for('dashboard'))

@app.route('/')
def home():
    
    return render_template('home.html')

@login_manager.user_loader
def user_loader(email):
    user_ref = db.collection('users').document(email)
    user_doc = user_ref.get()
    if not user_doc.exists:
        return None

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

    user_ref = db.collection('users').document(current_user.id)
    user_data = user_ref.get().to_dict()

    sleep_data = user_data.get('sleep', [])
    sleep_data.append({'date': date, 'hours': hours})

    user_ref.update({'sleep': sleep_data})
    return jsonify({'message': 'Sleep data recorded successfully'}), 201

@app.route('/physical_activity', methods=['POST'])
@login_required
def log_physical_activity():
    data = request.get_json()
    hours = data.get('hours')
    date = data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))

    if not hours:
        return jsonify({'error': 'Hours excercised is required'}), 400

    user_ref = db.collection('users').document(current_user.id)
    user_data = user_ref.get().to_dict()

    exercise_data = user_data.get('physical_activity', [])
    exercise_data.append({'date': date, 'hours': hours})

    user_ref.update({'physical_activity': exercise_data})
    return jsonify({'message': 'Exercise data recorded successfully'}), 201

@app.route('/food', methods=['POST'])
@login_required
def log_food():
    data = request.get_json()
    calories = data.get('calories')
    date = data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))

    if not calories:
        return jsonify({'error': 'Calories consumed is required'}), 400

    user_ref = db.collection('users').document(current_user.id)
    user_data = user_ref.get().to_dict()

    calories_data = user_data.get('calories', [])
    calories_data.append({'date': date, 'calories': calories})

    user_ref.update({'calories': calories_data})
    return jsonify({'message': 'Calories data recorded successfully'}), 201

@app.route('/journalling', methods=['POST'])
@login_required
def log_journalling():
    data = request.get_json()
    content = data.get('content')
    date = data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    user_ref = db.collection('users').document(current_user.id)
    user_data = user_ref.get().to_dict()

    content_data = user_data.get('journals', [])
    content_data.append({'date': date, 'content': content})

    user_ref.update({'journals': content_data})
    return jsonify({'message': 'Journal data recorded successfully'}), 201

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
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def send_dashboard_page():
    return render_template('dashboard.html', name=current_user.id)

@app.route('/articles', methods=['GET'])
def send_articles_page():
    pass

@app.route('/aboutus', methods=['GET'])
def send_aboutus_page():
    pass

@app.route('/community', methods=['GET'])
def send_community_page():
    pass

@app.route('/journalling', methods=['GET'])
def send_journalling_page():
    pass


if __name__ == '__main__':
    print(calculate_sleep_score('ass@ass.com'))
    app.run(debug=True)