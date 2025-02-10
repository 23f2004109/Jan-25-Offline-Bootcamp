from flask import Flask, render_template
from controller.database import db
from controller.models import *

app = Flask(__name__,template_folder='views')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)

with app.app_context():
    db.create_all()

    admin_role = Role.query.filter_by(name = 'admin').first()
    if not admin_role:
        admin_role = Role(
            name = 'admin',
            description = 'admin role'
        )

        db.session.add(admin_role)

    customer_role = Role.query.filter_by(name = 'customer').first()
    if not customer_role:
        customer_role = Role(
            name = 'customer',
            description = 'customer role'
        )

        db.session.add(customer_role)

    manager_role = Role.query.filter_by(name = 'manager').first()
    if not manager_role:
        manager_role = Role(
            name = 'manager',
            description = 'manager role'
        )

        db.session.add(manager_role)
    

    admin = User.query.filter_by(email = 'admin@gmail.com').first()
    if not admin:
        

        # admin = User(
        # name = 'admin',
        #     email = 'admin@gmail.com',
        #     password= '1234567890'
        # )

        # db.session.add(admin)


        # user = User.query.filter_by(email = 'admin@gmail.com').first()
        # role = Role.query.filter_by(name = 'admin').first()

        # user_role = UserRole(
        #     user_id = user.id,
        #     role_id = role.id
        # )
        # db.session.add(user_role)

    db.session.commit()




from controller.routes import *




if __name__ == '__main__':
 app.run(debug=True)




