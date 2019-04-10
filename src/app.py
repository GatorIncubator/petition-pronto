from flask import render_template, Flask, Response, redirect, url_for, request, abort, session


app = Flask(__name__)


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
    if email == "email" and password == "password":
        return redirect("/petitions")
    else:
        redirect("/login")


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
