from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField
from flask_wtf.file import FileField, FileAllowed

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trendy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

configure_uploads(app, photos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

"""
Add product table

"""

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    description = db.Column(db.String(500))
    image = db.Column(db.String(500))

"""
Create add product form using wtf

"""
class AddProduct(FlaskForm):
    name = StringField('Name')
    price = IntegerField('Price')
    stock = IntegerField('Stock')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[FileAllowed(IMAGES, 'Only images are accepted.')])



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product')
def product():
    return render_template('view-product.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/admin')
def admin():
    return render_template('admin/index.html', admin=True)

@app.route('/admin/add', methods=['GET', 'POST'])
def add():
    form = AddProduct()

    if form.validate_on_submit():
        print(form.name.data)
        print(form.price.data)
        print(form.stock.data)
        print(form.description.data)
        print(form.image.data)
    return render_template('admin/add-product.html', admin=True, form=form)

@app.route('/admin/order')
def order():
    return render_template('admin/view-order.html', admin=True)

if __name__ == '__main__':
    manager.run()


# export FLASK_APP=app.py FLASK_DEBUG=true
# python -m flask run

# python app.py db init
# to generate the table 
# python app.py db migrate

