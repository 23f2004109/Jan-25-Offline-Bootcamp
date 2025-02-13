from app import app
from flask import render_template, request, session, redirect, url_for, flash
from controller.models import * 

@app.route('/dashboard')
def home():
    return render_template('home.html') 

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
            flash('Please enter email and password')
            return render_template('login.html')
        
        email = User.query.filter_by(email = email).all()
        if not email:
            ## return error message
            flash('Email not found')
            return render_template('login.html')
        
        if email[0].password != password:
            ## return error message
            flash('Password incorrect')
            return render_template('login.html')
        
        session['user_email'] = email[0].email
        session['role'] = email[0].roles[0].name

        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    # session.pop('user_email', None)
    # session.pop('role', None)
    session.clear()
    return redirect(url_for('login'))  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')  

    if request.method == "POST":   
        name = request.form.get('name', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        role = request.form.get('role', None)
        confirm_password = request.form.get('confirm_password', None)

        # data validation

        if not name or not email or not password or not role or not confirm_password:
            flash('Please fill all fields')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Password does not match')
            return render_template('register.html')
        
        if User.query.filter_by(email = email).all():
            flash('Email already exists')
            return render_template('register.html')
        
        user = User(
            name = name,
            email = email,
            password = password,
            roles = [Role.query.filter_by(name = role).first()],
            roles = Role.query.filter_by(name = role).all()

        )

        db.session.add(user)
        db.session.commit()

        flash('User created successfully')
        return redirect(url_for('login'))


@app.route('/about')
def about():
    return 'The about page' 