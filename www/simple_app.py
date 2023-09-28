'''
https://code-boxx.com/search-results-python-flask/#sec-search
'''

from flask import Flask, jsonify, render_template, request, make_response
from flask.views import MethodView
from flask_simplelogin import SimpleLogin, get_username, login_required
import sqlite3

my_users = {
    "richard": {"password": "carbone", "roles": ["admin"]},
    "connor": {"password": "weeks", "roles": ["admin"]},
    "lee": {"password": "douglas", "roles": []},
    "mary": {"password": "jane", "roles": []},
    
}
HOST_NAME = "0.0.0.0"
HOST_PORT = 443
DBFILE = "ctic.db"

def check_my_users(user):
    """Check if user exists and its credentials.
    Take a look at encrypt_app.py and encrypt_cli.py
     to see how to encrypt passwords
    """
    user_data = my_users.get(user["username"])
    if not user_data:
        return False  # <--- invalid credentials
    elif user_data.get("password") == user["password"]:
        return True  # <--- user is logged in!

    return False  # <--- invalid credentials

def query_db(table,value,actor,malware):
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()
  print('test')
  cursor.execute(
    "SELECT * FROM "+table+" WHERE `value` LIKE ? AND `actor` LIKE ? AND `malware` LIKE ?",
    ("%"+value+"%", "%"+actor+"%", "%"+malware+"%",)
  )
  results = cursor.fetchall()
  print(results)
  conn.close()
  return results
  

app = Flask(__name__)
app.config.from_object("settings")
context = ('cert.pem', 'key.pem')

simple_login = SimpleLogin(app, login_checker=check_my_users)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/secret")
@login_required(username=["richard", "connor"])
def secret():
    return render_template("secret.html")


@app.route("/api", methods=["POST"])
@login_required(basic=True)
def api():
    return jsonify(data="You are logged in with basic auth")


def be_admin(username):
    """Validator to check if user has admin role"""
    user_data = my_users.get(username)
    if not user_data or "admin" not in user_data.get("roles", []):
        return "User does not have admin role"


def have_approval(username):
    """Validator: all users approved, return None"""
    return

#search goes here
@app.route("/search", methods=['GET', 'POST'])
@login_required(must=[be_admin, have_approval])
def search():
    #types = [' fqdn ', ' ipv4 ', ' hash ', ' url  ']
    if request.method == "POST":
        data = dict(request.form)
        print(data)
        table=data['type']
        value=data['value']
        actor=data['actor']
        malware=data['malware']
        print(table,value,actor,malware)
        results=query_db(table,value,actor,malware)
        print(len(results))
    else:
        results = []
    return render_template("search.html", results=results)


class ProtectedView(MethodView):
    decorators = [login_required]

    def get(self):
        return "You are logged in as <b>{0}</b>".format(get_username())


app.add_url_rule("/protected", view_func=ProtectedView.as_view("protected"))


if __name__ == "__main__":
    app.run(host=HOST_NAME, port=HOST_PORT, use_reloader=False, debug=False, ssl_context=context)
