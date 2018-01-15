
from flask import Flask, render_template,request,jsonify, flash, redirect
from datetime import datetime
import csh_ldap
import json
import requests
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import requests


app = Flask(__name__)
db = SQLAlchemy(app)

app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

requests.packages.urllib3.disable_warnings()




app.secret_key = 'shh, dont tell anyone'

class master(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    username = db.Column(db.String(50))
    victory = db.Column(db.String(2000))
    
    def __init__ (self, time, username, victory):
        self.time = datetime.now()
        self.username = username
        self.victory = victory
        
class moderated_owens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    username = db.Column(db.String(50))
    victory = db.Column(db.String(2000))
    
    def __init__ (self, time, username, victory):
        self.time = datetime.now()
        self.username = username
        self.victory = victory    

@app.route("/")
@auth.oidc_auth
def main():
   db.create_all()
   return render_template('index.html')

@app.route("/submission")
def submission():
   return render_template('submission.html')

@app.route("/submitted_owens")
@auth.oidc_auth
def submitted_owens():
    owens = master.query.all()
    return render_template('submitted_owens.html', submitted_owens=owens)

@app.route("/all_submitted_owens", methods=['GET'])
def all_submitted_owens():
    owens = master.query.order_by(owens.id.desc()).all()
    return jsonify(parse_as_json(owens))

@app.route("/owen_history", methods=['GET'])
def all_owens():
    owens = moderated_owens.query.all()
    return jsonify(parse_as_json(owens))

@app.route("/current_owen", methods=['GET'])
def current_owen():
     return jsonify(return_json(moderated_owens.query.order_by(moderated_owens.id.desc()).first()))

 
@app.route("/add_owen", methods = ['PUT'])
def add_owen():
   data = json.loads(request.data.decode('utf-8'))
   if data['username'] and data['victory']:
      owen_data = data['username']
      time_data = data['time']
      victory_data = data['victory']
      
      new_owen = master(username=owen_data, time=time_data, victory=victory_data)
      
      db.session.add(new_owen)
      db.session.flush()
      db.session.commit()
      return jsonify(return_json(new_owen))
   else:
       return "error, fields weren't full"



def return_json(owen):
    return {
        'username': owen.username,
        'time': owen.time,
        'victory': owen.victory,
    }

def parse_as_json(owens, owen_json=None):
    if owen_json is None:
        owen_json = []
    for owen in owens:
        owen_json.append(return_json(owen))
    return owen_json


if __name__ == "__main__":
    app.run()

application = app
