from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

DB_USER = "yc3515"
DB_PASSWORD = "73258qvz"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/w4111"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASEURI
db = SQLAlchemy(app)

class Event(db.Model):
    eid = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50))
    food_info = db.Column(db.String(50))
    title = db.Column(db.String(50))
    abstract = db.Column(db.Text)
    begin_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    organizations = db.relationship("Hold", back_populates = "event")

class Areas(db.Model):
    aid = db.Column(db.Integer, primary_key = True)
    aname = db.Column(db.String(50))

class Researcher(db.Model):
    rid = db.Column(db.Integer, primary_key = True)
    rname = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    citations = db.Column(db.String(50))
    publications = db.Column(db.String(50))
    researchers = db.relationship("Participate", back_populates = "holds")

class Organization(db.Model):
    oid = db.Column(db.Integer, primary_key = True)
    titel = db.Column(db.String(50), nullable = False)
    iid = db.Column(db.Integer, nullable = False)
    events = db.relationship("Hold", back_populates = "organization")
    institutions = db.relationship("Institution", back_populates = "organizations")

class Institution(db.Model):
    iid = db.Column(db.Integer, primary_key = True)
    iname = db.Column(db.String(50), nullable = False)


class Hold(db.Model):
    hid = db.Column(db.Integer, primary_key = True)
    oid = db.Column(db.Integer, db.ForeignKey(organization.oid), nullable = False)
    eid = db.Column(db.Integer, db.ForeignKey(event.eid), nullable = False)
    organization = db.relationship("Event", back_populates = "organizations")
    holds = db.relationship("Organization", back_populates = "events")
    researchers = db.relationship("Participate", back_populates = "hold")

class Participate(db.Model):
    hid = db.Column(db.Integer, db.ForeignKey(hold.hid), primary_key = True)
    rid = db.Column(db.Integer, db.ForeignKey(researcher.rid), primary_key = True)
    ptype = db.Column(db.String(50), db.CheckConstraint('ptype in ('audience', 'host', 'speaker')')
    researcher  = db.relationship("Researcher", back_populates = "holds")
    hold = db.relationship("Hold", back_populates = "researchers")
    

@app.route('/')
def index():
    posts = event.query.order_by(event.begin_time.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add')
def add():
    return render_template('add.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
