from app import app
from flask import render_template, request, session, redirect, url_for, flash
from controller.models import * 

@app.route('/')
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
        
        if email[0].flag:
            flash('User is deactivated')
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
            
        )

        db.session.add(user)
        db.session.commit()

        flash('User created successfully')
        return redirect(url_for('login'))
    
@app.route('/manage_users')
def manage_users():
    if not session.get('user_email',None) or session.get('role', None) != 'admin':
        flash('Unauthorized Access')
        return redirect(url_for('home'))
    customers = User.query.filter(User.roles.any(name='customer')).all()
    store_managers = User.query.filter(User.roles.any(name='manager')).all()
    return render_template('manage_users.html', customers=customers, store_managers=store_managers)


@app.route('/delete_user/<int:id>')
def delete_user(id):
    if not session.get('user_email',None) or session.get('role', None) != 'admin':
        flash('Unauthorized Access')
        return redirect(url_for('home'))
    
    user = User.query.get(id)

    if not user:
        flash('User not found')
        return redirect(url_for('manage_users'))
    
    db.session.delete(user)
    db.session.commit()

    flash('User deleted successfully')
    return redirect(url_for('manage_users'))

@app.route('/deactivate_user/<int:id>')
def deactivate_user(id):
    if not session.get('user_email',None) or session.get('role', None) != 'admin':
        flash('Unauthorized Access')
        return redirect(url_for('home'))
    
    user = User.query.get(id)

    if not user:
        flash('User not found')
        return redirect(url_for('manage_users'))
    
    user.flag = True
    db.session.commit()

    flash('User deactivated successfully')
    return redirect(url_for('manage_users'))


@app.route('/activate_user/<int:id>')
def activate_user(id):
    if not session.get('user_email',None) or session.get('role', None) != 'admin':
        flash('Unauthorized Access')
        return redirect(url_for('home'))
    
    user = User.query.get(id)

    if not user:
        flash('User not found')
        return redirect(url_for('manage_users'))
    
    if not user.flag:
        flash('User is already active')
        return redirect(url_for('manage_users'))
    
    user.flag = False
    db.session.commit()

    flash('User activated successfully')
    return redirect(url_for('manage_users'))




@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if not session.get('user_email',None) or session.get('role', None) != 'admin':
        flash('Unauthorized Access')
        return redirect(url_for('home'))
    
    if request.method == "GET":
        return render_template('add_category.html')
    
    if request.method == "POST":
        name = request.form.get('name', None)
        description = request.form.get('description', None)

        if not name or not description:
            flash('Please fill all fields')
            return render_template('add_category.html')
        
        category = Categories.query.filter_by(name = name).all()
        if category:
            flash('Category already exists')
            return render_template('add_category.html')
        
        category = Categories(
            name = name,
            description = description
        )

        db.session.add(category)
        db.session.commit()

        flash('Category added successfully')
        return redirect(url_for('add_category'))
    
@app.route('/edit_category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    if not session.get('user_email',None) or session.get('role', None) != 'admin':
        flash('Unauthorized Access')
        return redirect(url_for('home'))
    
    category = Categories.query.get(id)
    if not category:
        flash('Category not found')
        return redirect(url_for('home'))
    
    if request.method == "GET":
        return render_template('edit_category.html', category=category)
    
    if request.method == "POST":
        name = request.form.get('name', None)
        description = request.form.get('description', None)

        new_category = Categories.query.filter_by(name = name).first()

        if new_category and new_category.id != category.id:
            flash('Category with this name already exists')
            return render_template('edit_category.html', category=category)
        

        if name:
            category.name = name

        if description:
            category.description = description

        db.session.commit()

        flash('Category updated successfully')
        return redirect(url_for('home'))
    

@app.route('/delete_category/<int:id>')
def delete_category(id):
    if not session.get('user_email',None) or session.get('role', None) != 'admin':
        flash('Unauthorized Access')
        return redirect(url_for('home'))
    
    category = Categories.query.get(id)

    if not category:
        flash('Category not found')
        return redirect(url_for('home'))
    
    db.session.delete(category)
    db.session.commit()

    flash('Category deleted successfully')
    return redirect(url_for('home'))

