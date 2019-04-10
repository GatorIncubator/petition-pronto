from flask import render_template, Flask, Response, redirect, url_for, request, abort, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route("/", methods=["GET"])
def home_redirect():
    return redirect("/home")


@app.route("/home", methods=["GET"])
def home_get():
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        return redirect("/petitions")


@app.route("/login", methods=["GET"])
def login_get():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect("/petitions")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form['email']
    password = request.form['password']
    print("HI")
    if email == "email@email.com" and password == "password":
        session['logged_in'] = True
        session['email'] = email
        return redirect("/petitions")
    else:
        return redirect("/invalid_login")


@app.route("/invalid_login", methods=["GET"])
def invalid_login_get():
    return render_template("invalid_login.html")


@app.route("/petitions", methods=["GET"])
def petitions_get():
    if session.get('logged_in'):
        return render_template('petitions.html')
    else:
        return redirect("/home")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
