from flask import Flask, render_template
from csh_ldap import CSHLDAP


app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()

application = app
