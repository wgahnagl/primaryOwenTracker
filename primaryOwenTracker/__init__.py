from flask import Flask, render_template
import csh_ldap

app = Flask(__name__)


@app.route("/")
def main():
   return render_template('index.html')

@app.route("/submission")
def submission():
   return render_template('submission.html')

if __name__ == "__main__":
    app.run()

application = app
