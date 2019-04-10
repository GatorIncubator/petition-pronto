from flask import render_template, Flask, Response, redirect, url_for, request, abort


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home_get():
    return render_template('home.html')


if __name__ == "__main__":
    app.run()
