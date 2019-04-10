from flask import render_template, Flask, Response, redirect, url_for, request, abort


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home_redirect():
    return redirect("/home")


@app.route("/home", methods=["GET"])
def home_get():
    return render_template('home.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run()
