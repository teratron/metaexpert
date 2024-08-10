"""Expert Application
"""
from _logger import getLogger
from flask import Flask, render_template, request, flash, redirect, jsonify

logger = getLogger(__name__)
app = Flask(__name__)


@app.route("/")
def index():
    title = "Home"
    return render_template("view.home.tmpl", title=title)


@app.route("/about")
def about():
    title = "About"
    return render_template("view.about.tmpl", title=title)


@app.route("/hello")
def hello():
    return "<h1>Hello, World!</h1>"


@app.errorhandler(404)
def not_found(error):
    return render_template('view.error.tmpl', error=error), 404


if __name__ == "__main__":
    logger.info("start app")

    app.run(port=5001, debug=True)

    logger.info("finish app")
