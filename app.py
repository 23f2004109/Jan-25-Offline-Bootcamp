from flask import Flask, render_template
from controller.database import db
from controller.models import *

app = Flask(__name__,template_folder='views')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)

with app.app_context():
    db.create_all()

    

from controller.routes import *




if __name__ == '__main__':
 app.run(debug=True)




