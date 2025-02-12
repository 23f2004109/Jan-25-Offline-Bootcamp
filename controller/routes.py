from app import app
from flask import render_template, request, session, redirect
from controller.models import * 

@app.route('/<string:name>')
def home(name):
    print(name)
    return render_template('home.html', t_name = name) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    
    if request.method == "POST":
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        #data vaildation

        if not email or not password:
            # return error message
            return render_template('login.html')
        
        email = User.query.filter_by(email = email).all()
        if not email:
            ## return error message
            return render_template('login.html')
        
        if email.password != password:
            ## return error message
            return render_template('login.html')
        
        session['user_email'] = email
        session['role'] = email.roles[0].name

        return redirect()
             


@app.route('/about')
def about():
    return 'The about page' 