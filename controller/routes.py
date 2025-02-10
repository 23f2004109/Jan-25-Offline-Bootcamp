from app import app
from flask import render_template

@app.route('/<string:name>')
def home(name):
    print(name)
    return render_template('home.html', t_name = name) 

@app.route('/about')
def about():
    return 'The about page' 