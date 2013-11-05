from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional
import os

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else 'postgresql://localhost:5432/bio'
application.config['CSRF_ENABLED'] = True
application.config['SECRET_KEY'] = 'rahasiabesar'

db = SQLAlchemy(application) 

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    password = db.Column(db.String)
    email = db.Column(db.String(100), unique=True)

    time_registered = db.Column(db.DateTime)
    tagline = db.Column(db.String(255))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(255))

    def __init__(self, username = None, password = None, email = None, firstname = None, lastname = None, tagline = None, bio = None, avatar = None):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.tagline = tagline
        self.bio = bio
        self.avatar = avatar

class SignupForm(Form):
    email = TextField('Email address', validators=[
            Required('Please provide a valid email address'),
            validators.Length(min=6, message=(u'Email address too short')),
            validators.Email(message=(u'That\'s not a valid email address.'))
            ])
    password = PasswordField('Pick a secure password', validators=[
            Required(),
            validators.Length(min=6, message=(u'Please give a longer password'))           
            ])
    username = TextField('Choose your username', validators=[Required()])
    agree = BooleanField('I agree all your <a href="/static/tos.html">Terms of Services</a>', validators=[Required(u'You must accept our Terms of Service')])

@application.route('/')
@application.route('/<username>')
def index(username = None):
    if username is None:
        return render_template('index.html', page_title = 'Biography just for you!')
    
    user = Users.query.filter_by(username=username).first()
    if user is None:
        user = Users()
        user.username = username
        user.firstname = 'Batman, is that you?'
        user.lastname = ''
        user.tagline = 'Tagline of how special you are'
        user.bio = 'Explain to the rest of the world, why you are the very most unique person to look at'
        user.avatar = '/static/batman.jpeg'
        return render_template('themes/water/bio.html', page_title = 'Claim this name : ' + username, user = user)
    return render_template('themes/water/bio.html', page_title = user.firstname + ' ' + user.lastname, user = user)

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = SignupForm(request.form)
        if form.validate():
            pass
        else:
            return render_template('signup.html', form = form, page_title = 'Signup to Bio Application')
    return render_template('signup.html', form = SignupForm(), page_title = 'Signup to Bio Application')


def dbinit():
    db.drop_all()
    db.create_all()
    db.session.add(Users(username='ekowibowo', firstname='Eko', 
                         lastname='Suprapto Wibowo', password='rahasia',
                         email='swdev.bali@gmail.com', 
                         tagline='A cool coder and an even cooler Capoeirista', 
                         bio = 'I love Python very much!', 
                         avatar = '/static/avatar.png'))
    db.session.commit()

if __name__ == '__main__':
    dbinit()
    application.run(debug=True, host="0.0.0.0", port=8888)
