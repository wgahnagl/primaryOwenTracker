from flask import Flask, render_template,request,jsonify
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

class master(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    username = db.Column(db.String(50))
    victory = db.Column(db.String(2000))
    
    def __init__ (self, time, username, victory):
        self.time = datetime.now()
        self.username = username
        self.victory = victory    

@app.route("/")
def main():
   db.create_all()
   return render_template('index.html')

@app.route("/submission")
def submission():
   return render_template('submission.html')

@app.route("/get_primary_owen", methods=['GET'])
def all_owens():
    owens = moderated_owens.query.all()
    return jsonify(parse_as_json(owens))

@app.route("/add_owen", methods = ['PUT'])
def add_owen():
   data = json.loads(request.data.decode('utf-8'))
   if data['username'] and data['victory']:
      owen_data = data['username']
      time_data = data['time']
      victory_data = data['victory']
      new_owen = master(username= owen_data, time=time_data, victory=victory_data)
      
      db.session.add(new_owen)
      db.session.flush()
      db.session.commit()
      return jsonify(return_json(new_owen))

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
