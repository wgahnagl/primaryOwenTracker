from flask import Flask, render_template
from csh_ldap import CSHLDAP


app = Flask(__name__)

ldap = CSHLDAP(app.config["LDAP_BIND_DN"], app.config["LDAP_BIND_PW"])

from primaryOwenTracker.ldap import ldap_is_eboard, ldap_is_rtp


@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()

application = app
