from flask import render_template
from app import app

@app.route("/")
@app.route("/index")
def index():
    user = {'username': 'Jenn'}
    return render_template('intro.html', title='Home', user=user)