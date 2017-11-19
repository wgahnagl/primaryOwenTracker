from flask import Flask, render_template,request,jsonify
from datetime import datetime
import csh_ldap
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
import requests
"""TODO: you need to get the submission page working fully, pushing things to the put request, and then build the database. 
after that you need to get ldap working, and have the submission page be a dropdown menu with all CSHers with a search """


app = Flask(__name__)
db = SQLAlchemy(app)


class master(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    username = db.Column(db.String(50))
    victory = db.Column(db.String(2000))

@app.route("/")
def main():
   return render_template('index.html')
   


@app.route("/submission")
def submission():
   return render_template('submission.html')

@app.route("/get_from_database", methods=['GET'])
def all_owens():
    owens = master.query.all()
    return jsonify(parse_as_json(owens))


@app.route("/add_owen", methods = ['PUT'])
def add_owen():
   db.create_all()
    
   data = json.loads(request.data.decode('utf-8'))
   if data['username'] and data['victory']:
      owen_data = data['username']
      victory_data = data['victory']
      new_owen = master(time=datetime.now(), username=owen_data, victory=victory_data)
      
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
        owen_json.append(return_json(owens))
    return owen_json


if __name__ == "__main__":
    app.run()

application = app
