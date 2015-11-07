from __future__ import print_function
import imghdr
import os
from flask import Flask, render_template, flash, url_for, redirect
from flask.ext.bootstrap import Bootstrap
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask.ext.wtf import Form
from wtforms import FileField, SubmitField, StringField, TextAreaField, RadioField, SelectField, ValidationError
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

    def validate_image_file(self, field):
        if len(field.data.filename) != 0:
            if field.data.filename[-4:].lower() != '.jpg' and field.data.filename[-4:].lower() != '.png' :
                raise ValidationError('Invalid file extension: please select a jpg or png file')

            if imghdr.what(field.data) != 'jpeg' and imghdr.what(field.data) != 'png':
                raise ValidationError('Invalid image format: please select a jpg or png file')


@app.route('/')
def show_categories():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('index.html', categories=categories)


@app.route('/items/<int:category_id>')
def items(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    #print ("category {}".format(category.name))
    items=session.query(CategoryItem).filter_by(category_id=category_id)
    #print ('items {}'.format(items))
    return render_template('items.html', items=items, category=category )


@app.route('/item/<int:item_id>')
def show_item(item_id):
    #print ("show item")
    item=session.query(CategoryItem).filter_by(id=item_id).one()
    #print ("item = {}".format(item))
    return render_template('details.html', item=item)


@app.route('/new/item/<int:category_id>', methods=['GET','POST'])
def new_item(category_id):
    print ('category_id {}'.format(category_id))
    category = session.query(Category).filter_by(id=category_id).one()
    form = CatalogItemForm()

    if form.validate_on_submit():
        #print('foo')
        if form.image_file.data.filename:
            filename = form.image_file.data.filename
            item_image = 'images/' + form.image_file.data.filename
            form.image_file.data.save(os.path.join(app.static_folder,item_image))
        else:
            filename = 'no-image.png'

        print ('cat id {}'.format(category_id))

        newItem = CategoryItem(
            name=form.item_name.data,
            description=form.item_desc.data,
            image=filename,
            category_id=category_id,
            user_id = 1
        )
        #print('new item created')
        session.add(newItem)
        #print ('new item added')
        session.commit()
        flash('New Item {} Successfully Created'.format(newItem.name))
        return redirect(url_for('show_categories'))

    #print ('2')
    return render_template('newitem.html', form=form, category_name=category.name)

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
    app.run(debug=True)
