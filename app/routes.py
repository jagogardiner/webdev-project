""" Flask website routes """
from flask import render_template, request
from .main import app


@app.route("/")
@app.route("/home")
def home():
    user = {'username': 'Jago'}
    return render_template('home.html', title='Home', user=user)


@app.route("/locations")
def locations():
    return render_template('locations.html')


@app.route("/test")
def test():
    return render_template('test.html')
