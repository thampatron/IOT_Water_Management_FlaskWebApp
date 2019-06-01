
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import datetime



main = Blueprint('main', __name__)

@main.route('/')
def index():
    labels = [1,2,3,4,5,6,7,8]
    data = [1,2,2,3,4,4,7,8]
    date_setting = request.args.get('date_setting') if request.args.get('date_setting') else 'Day'
    print(date_setting)
    return render_template('index.html', labels=labels,date_settin=date_setting, data=data)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/changedate' , methods=['POST'])
@login_required
def changedate():
    date_setting = request.form.get('date')
    print(date_setting)
    now = datetime.datetime.now()
    print(now.strftime('%Y-%m-%d %H'))
    hour_ago = now - datetime.timedelta(hours=1, minutes=0)
    print(hour_ago)
    labels = [1,2,3,4,5,6,7,8]
    data = [1,2,2,3,4,4,7,0,9]
    
    return redirect(url_for('main.index', date_setting=date_setting))

"""@main.route('/addnode', methods=['POST'])
@login_required
def addnode():"""
