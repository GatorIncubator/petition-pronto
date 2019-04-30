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


@app.route("/home", methods=["POST"])
def home_post():
    if not session.get('logged_in'):
        student_email = request.form['student_email']
        name = request.form['student_name']
        description = request.form['petiton_description']
        department = request.form['department-selection']
        database_handler.add_petition(name, student_email, description, department)
        return redirect('/success')
    else:
        return redirect("/petitions")


@app.route("/success", methods=["GET"])
def success_get():
    if not session.get('logged_in'):
        return render_template('success.html')
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
    valid, admin = login_handler.validate_user(email, password)
    if valid:
        session['logged_in'] = True
        session['email'] = email
        session['admin'] = admin
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
            database_handler.change_password(session.get('email'), password)
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


@app.route("/create_account", methods=["GET"])
def create_account_get():
    if session.get('logged_in') and session.get("admin"):
        return render_template("create_account.html")
    else:
        return redirect("/home")


@app.route("/create_account", methods=["POST"])
def create_account_post():
    if session.get('logged_in') and session.get("admin"):
        email = request.form['email']
        password = request.form['password']
        department = request.form['department-selection']
        role = request.form['role']
        database_handler.create_account(email, password, role, department)
    return redirect("/petitions")


@app.route("/petitions", methods=["GET"])
def petitions_get():
    if session.get('logged_in'):
        petitions = database_handler.get_petitions(session['email'])
        out_petitions = list()
        for petition in petitions:
            new_petition = {'id':petition[3],'name':petition[0],'email':petition[1],'department':petition[2]}
            out_petitions.append(new_petition)
        return render_template("petitions.html", petitions=out_petitions, admin=session["admin"])
    else:
        return redirect("/home")


@app.route("/petitions/<id>", methods=["GET"])
def petitions_inspect_get(id):
    if session.get('logged_in'):
        petition = database_handler.get_petition_info(id)
        new_petition_info = {'id':petition[4],'name':petition[0],'email':petition[1],'department':petition[3],'content':petition[2]}
        return render_template("petition_info.html", petition_info=new_petition_info)
    else:
        return redirect("/home")


@app.route("/petitions/<id>", methods=["POST"])
def petitions_inspect_post(id):
    if session.get('logged_in'):
        approved = request.form['approved']
        approved = approved == "approved"
        database_handler.submit_decision(id, approved, session['email'])
        return redirect("/petitions")
    else:
        return redirect("/home")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
