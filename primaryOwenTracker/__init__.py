from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask import Flask, render_template, redirect, session, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from functools import wraps
import csh_ldap

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))
app.secret_key = 'shh, dont tell anyone'
APP_CONFIG = ProviderConfiguration(issuer=app.config["OIDC_ISSUER"],
                                   client_metadata=ClientMetadata(app.config["OIDC_CLIENT_CONFIG"]['client_id'],
                                                                  app.config["OIDC_CLIENT_CONFIG"]['client_secret']))
auth = OIDCAuthentication({'app': APP_CONFIG}, app)
_ldap = csh_ldap.CSHLDAP(app.config["LDAP_BIND_DN"], app.config["LDAP_BIND_PASS"])


class Owens(db.Model):
    __tablename__ = 'Owens'
    username = db.Column(db.String(50), ForeignKey('Users.uid'), primary_key=True)
    score = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    def __init__(self, username, score, time):
        self.username = username
        self.score = score
        self.timeOfOwening = time


class Users(db.Model):
    __tablename__ = 'Users'
    uid = db.Column(db.String(50), primary_key=True)
    modifier = db.Column(db.Integer, default=10)

    def __init__(self, uid, modifier):
        self.uid = uid
        self.modifier = modifier


class Submissions(db.Model):
    submitter = db.Column(db.String(50), ForeignKey('Users.uid'))
    argument = db.Column(db.String(2000))
    suggestedPoints = db.Column(db.Integer)
    time = db.Column(db.DateTime, primary_key=True)
    owen = db.Column(db.String(50), ForeignKey('Owens.username'))
    accepted = db.Column(db.Boolean)

    def __init__(self, submitter, argument, suggestedpoints, time, owen, accepted):
        self.submitter = submitter
        self.argument = argument
        self.suggestedPoints = suggestedpoints
        self.time = time
        self.owen = owen
        self.accepted = accepted


def before_request(func):
    """
    Credit to Liam Middlebrook and Ram Zallan
    https://github.com/liam-middlebrook/gallery
    also credit to Devin and Joel who wrote packet, where I stole this function from lmao
    """

    @wraps(func)
    def wrapped_function(*args, **kwargs):
        uid = str(session["userinfo"].get("preferred_username", ""))

        info = {
            "realm": "csh",
            "uid": uid
        }

        kwargs["info"] = info
        return func(*args, **kwargs)

    return wrapped_function


@app.route("/")
@auth.oidc_auth('app')
def index():
    return redirect(url_for("main"), 302)


@app.route("/main")
@auth.oidc_auth('app')
@before_request
def main(info=None):
    db.create_all()
    return render_template('index.html', info=info)


@app.route("/submit")
@auth.oidc_auth('app')
@before_request
def submit(info=None):
    return render_template('submit.html', info=info)


@app.route("/admin")
@auth.oidc_auth('app')
@before_request
def admin(info=None):
    if info['uid'] != 'wgahnagl':
        return redirect(url_for("main"), 302)
    return render_template('admin.html', info=info)


@app.route("/logout")
@auth.oidc_logout
def logout():
    return redirect("http://csh.rit.edu", 302)


if __name__ == "__main__":
    app.run()

application = app
