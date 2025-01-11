from mail import sendmail 
import os
from dotenv import load_dotenv



import jinja2
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import secrets
import uuid

#load_dotenv()
#sendmail(os.getenv('SMTPUSERNAME'),"<insert email id>","Subject","Text Material",os.getenv('SMTPPASS'))

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


users = {'foo@bar.tld': {'password': 'secret'}}
forumData = [{'name':'foo','heading':'testMessageOne','likes':69,'id':uuid.uuid4()}]
class User(UserMixin):
    def __init__(self, id, password=None):
        self.id = id
        self.password = password

@app.route('/')
def home():
    return render_template('home.html')

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User(email)
    return user

@app.route('/login',methods = ['GET','POST'])
def login():
    if(request.method == 'POST'):
        email = request.form['email']
        if(email in users and request.form['password']==users[email]['password']):
            user = User(email)
            login_user(user)
            return redirect(url_for('dashboardLoad'))
        return 'BAD LOGIN'
    else:
        return render_template("login.html")

@app.route('/about')
def aboutus():
    return render_template("about.html")

@app.route('/dashboard')
@login_required
def dashboardLoad():
    return render_template("dashboard.html")

@app.route('/sleep')
@login_required
def sleep_dboard():
    return "SLEEP"

@app.route('/physical_activity')
@login_required
def physical_dboard():
    return "PHYSICAL ACTIVITY"

@app.route('/food')
@login_required
def food_dboard():
    return "FOOD"

@app.route('/emotions')
@login_required
def emotions_dboard():
    return "Emotions"

@app.route('/journalling')
@login_required
def journalling_dboard():
    return "JOURNALLING"

@app.route('/community')
@login_required
def community_dboard():
    return render_template("community.html",posts=forumData)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    #print("DEBIG")
    return redirect(url_for('aboutus'))


if __name__ == '__main__':
    app.run(debug=False)
