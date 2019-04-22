from flask import render_template, Flask, Response, redirect, url_for, request, abort, session
import os
import login_handler
import database_handler


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
    valid = login_handler.validate_user(email, password)
    if valid:
        session['logged_in'] = True
        session['email'] = email
        return redirect("/petitions")
    else:
        return redirect("/invalid_login")


@app.route("/invalid_login", methods=["GET"])
def invalid_login_get():
    return render_template("invalid_login.html")


@app.route("/logout", methods=["GET"])
def logout_get():
    session.clear()
    return redirect("/home")


@app.route("/change_password", methods=["GET"])
def change_password_get():
    if session.get('logged_in'):
        return render_template("change_password.html")
    else:
        return redirect("/home")


@app.route("/change_password", methods=["POST"])
def change_password_post():
    if session.get('logged_in'):
        password = request.form['password']
        confirm_password = request.form["confirm_password"]
        if password == confirm_password:
            # database_handler.update_password(session.get('email'), new_password)
            print(password)
            return redirect("/petitions")
        else:
            return redirect("/invalid_confirmation")
    else:
        return redirect("/home")


@app.route("/invalid_confirmation", methods=["GET"])
def invalid_confirmation_get():
    if session.get('logged_in'):
        return render_template("invalid_confirmation.html")
    else:
        return redirect("/home")


@app.route("/petitions", methods=["GET"])
def petitions_get():
    if session.get('logged_in'):
        # petitions = database_handler.get_petitions(session['email'])
        petitions = [{'id':1,'name':"Austin Bristol",'email':"bristola@allegheny.edu",'department':'Computer Science'},{'id':2,'name':'Bob','email':'bob@allegheny.edu','department':'Computer Science'}]
        return render_template("petitions.html", petitions=petitions)
    else:
        return redirect("/home")


@app.route("/petitions/<id>", methods=["GET"])
def petitions_inspect_get(id):
    if session.get('logged_in'):
        # petition_info = database_handler.get_petition_info(id)
        petition_info = {'id':id,'name':"Austin Bristol",'email':"bristola@allegheny.edu",'department':'Computer Science','content':'This is some petition for something.'}
        return render_template("petition_info.html", petition_info=petition_info)
    else:
        return redirect("/home")


@app.route("/petitions/<id>", methods=["POST"])
def petitions_inspect_post(id):
    if session.get('logged_in'):
        approved = request.form['approved']
        print(approved)
        return redirect("/petitions")
    else:
        return redirect("/home")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
