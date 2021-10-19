""" Flask website routes """
from flask import render_template
from app import app

@app.route("/")
@app.route("/home")
def home():
    """ renders homepage"""
    user = {'username': 'Jago'}
    return render_template('home.html', title='Home', user=user)

@app.route("/login")
def login():
    """ renders login """
    return render_template('login.html')
