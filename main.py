""" main function for flask server """
from app import app
app.config['TEMPLATES_AUTO_RELOAD'] = True
if __name__ == "__main__":
    app.run(debug=False)
