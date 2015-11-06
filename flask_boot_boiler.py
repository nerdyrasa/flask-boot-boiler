from __future__ import print_function
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask.ext.wtf import Form
from wtforms import FileField, SubmitField, StringField, TextAreaField, RadioField
from catalog_db_setup import Base, Category, CategoryItem, User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret'
bootstrap = Bootstrap(app)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class CatalogItemForm(Form):

    item_name = StringField('Name')

    item_desc = TextAreaField('Description')

    image_file = FileField('Image file')

    submit = SubmitField('Submit')



class Bogus:
    print ('this is bogus')


@app.route('/')
def show_categories():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('index.html', categories=categories)


@app.route('/items/<int:category_id>')
def items(category_id):
    #category = session.query(Category).filter_by(category_id=category_id).one()
    print ("show all the items")
    items=session.query(CategoryItem).filter_by(category_id=category_id)
    print ('items {}'.format(items))
    return render_template('items.html', items=items)


@app.route('/item/<int:item_id>')
def show_item(item_id):
    print ("show item")
    item=session.query(CategoryItem).filter_by(id=item_id).one()
    print ("item = {}".format(item))
    return render_template('details.html', item=item)


@app.route('/new/item/<int:category_id>', methods=['GET','POST'])
def new_item(category_id):
    print ('********* 1 **************')
    form = CatalogItemForm()
    if form.validate_on_submit():
        print('foo')
    else:
        print('bar')
    print ('2')
    return render_template('newitem.html', form=form)

class SimpleForm(Form):
    example = RadioField('Label', choices=[('value','description'),('value_two','whatever')])


@app.route('/example',methods=['post','get'])
def hello_world():
    form = SimpleForm()
    if form.validate_on_submit():
        print (form.example.data)
    else:
        print (form.errors)
    return render_template('example.html',form=form)


if __name__ == '__main__':
    app.run()
