
from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import datetime
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'thampatron'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

lbls = []
data = []

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


@login_manager.user_loader
def load_user(user_id):
    
    return User.query.get(int(user_id))

# blueprint for auth routes in our app



@app.route('/')
def index():
    
    labels = [1,2,3,4,5,6,7,8]
    data = [[10,20,20,30,40,40,70,80,60,40],[20,20,20,30,40,40,80,80,70,70],[10,10,20,30,40,40,50,60,40,30],[10,10,30,40,50,40,70,60,50,10],[90,80,70,50,40,30,20,10,10,10]]
    now = datetime.datetime.now()
    oldtime = now
    lbls = []
    for i in range(0,10):
        lbls.append(oldtime.strftime('%H:%M %d-%b'))
        oldtime = oldtime - datetime.timedelta(hours=0, minutes=15)
    lbls.reverse()
    rqst = request.args.get('rqst')
    if rqst is None:
        sensor = "error"
    else:
        sensor = rqst

    print (rqst)
    date_setting = request.args.get('date_setting') if request.args.get('date_setting') else 'Day'
    print(date_setting)
    return render_template('index.html', labels=lbls,date_settin=date_setting, data=data, sensor=sensor)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route('/changedate' , methods=['POST'])
@login_required
def changedate():
    date_setting = request.form.get('date')
    print(date_setting)
    now = datetime.datetime.now()
    print(now.strftime('%Y-%m-%d %H'))
    hour_ago = now - datetime.timedelta(hours=1, minutes=0)
    print(hour_ago)
    oldtime = now
    lbls = []
    for i in range(0,10):
        lbls.append(oldtime.strftime('%h, %d, %m'))
        oldtime = oldtime - datetime.timedelta(hours=0, minutes=15)
    print(lbls)
    labels = [1,2,3,4,5,6,7,8]
    data = [1,2,2,3,4,4,7,0,9]
    
    return redirect(url_for('index', date_setting=date_setting))

@app.route('/addnode',methods=['GET','POST'])
def addnode():
    data = request.get_json()
    return redirect(url_for('index'))

@app.route('/sensor', methods=['GET','POST'])
def sensor():
    rqst = request.json
    sensor = rqst['payload_fields']['first']
    return redirect(url_for('index', rqst=sensor))
    
    # data = request.json['payload_fields']
    # word = data['version']    

    # return jsonify({'result' : word})

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('profile'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    print('PASS1')
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: 
        flash('Email address already in exists.')
        return redirect(url_for('signup'))
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    print('PASS')
    db.session.add(new_user)
    db.session.commit()

    #return redirect(url_for('app.login'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    return redirect(url_for('index'))


"""@main.route('/addnode', methods=['POST'])
@login_required
def addnode():"""

if __name__ == '__main__':
    app.run()