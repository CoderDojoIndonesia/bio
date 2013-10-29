from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else 'postgresql://localhost:5432/bio'

db = SQLAlchemy(application) 

class Users(db.Model,object):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    password = db.Column(db.String)
    email = db.Column(db.String(100), unique=True)

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

@application.route('/')
@application.route('/<username>')
def index(username = None):
    if username is None:
        return render_template('themes/water/index.html', page_title = 'Biography just for you!')
    
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

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.add(Users(username='ekowibowo', firstname='Eko', lastname='Suprapto Wibowo', password='rahasia', email='swdev.bali@gmail.com', tagline='A cool coder and an even cooler Capoeirista', bio = 'Amazingly created creature', avatar = '/static/avatar.png'))
    db.session.commit()
    application.run(debug=True, host="0.0.0.0", port=8888)
