""" Flask website routes """
from flask import render_template, request
from app import app

@app.route("/")
@app.route("/home")
def home():
    user = {'username': 'Jago'}
    return render_template('home.html', title='Home', user=user)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        _username = request.form['username']
    return render_template('signup.html')

@app.route("/locations")
def test():
    return render_template('locations.html')
