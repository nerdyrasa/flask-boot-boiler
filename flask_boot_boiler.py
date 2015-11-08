from __future__ import print_function
import imghdr
import os
from flask import Flask, render_template, flash, url_for, redirect, request
from flask.ext.bootstrap import Bootstrap
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask.ext.wtf import Form
from wtforms import FileField, SubmitField, StringField, TextAreaField, ValidationError
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
    name = StringField('Name')
    description = TextAreaField('Description')
    image = FileField('Image file')
    submit = SubmitField('Submit')

    def validate_image_file(self, field):
        if len(field.data.filename) != 0:
            if field.data.filename[-4:].lower() != '.jpg' and field.data.filename[-4:].lower() != '.png':
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
    items = session.query(CategoryItem).filter_by(category_id=category_id)
    return render_template('items.html', items=items, category=category)


@app.route('/item/<int:item_id>')
def show_item(item_id):
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    return render_template('details.html', item=item)


@app.route('/new/item/<int:category_id>', methods=['GET', 'POST'])
def new_item(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    form = CatalogItemForm()

    if form.validate_on_submit():
        if form.image.data.filename:
            filename = form.image.data.filename
            item_image = 'images/' + filename
            form.image.data.save(os.path.join(app.static_folder, item_image))
        else:
            filename = 'no-image.png'

        new_item = CategoryItem(
            name=form.name.data,
            description=form.description.data,
            image=filename,
            category_id=category_id,
            user_id=1
        )
        session.add(new_item)
        session.commit()
        flash('New Item {} Successfully Created'.format(new_item.name))
        return redirect(url_for('show_categories'))

    return render_template('newitem.html', form=form, category_name=category.name)


@app.route('/edit/item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):

    edited_item = session.query(CategoryItem).filter_by(id=item_id).one()

    form = CatalogItemForm(obj=edited_item)

    if form.validate_on_submit():
        if form.name.data:
            edited_item.name = form.name.data
        if form.description.data:
            edited_item.description = form.description.data
        if form.image.data.filename:
            filename = form.image.data.filename
            edited_item.image = filename
            item_image = 'images/' + filename
            form.image.data.save(os.path.join(app.static_folder, item_image))
        session.add(edited_item)
        session.commit()
        flash('Item successfully edited: {}'.format(edited_item.name))
        return redirect(url_for('show_categories'))

    return render_template('edititem.html', form=form, image=edited_item.image)


@app.route('/delete/item/<int:item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    item_to_delete = session.query(CategoryItem).filter_by(id=item_id).one()
    form = Form()
    if request.method=='POST':
        session.delete(item_to_delete)
        name = item_to_delete.name
        session.commit()
        flash('Item successfully deleted:{}'.format(name))
        return redirect(url_for('show_categories'))
    else:
        print('delete')

        return render_template('deleteitem.html', form=form, name=item_to_delete.name)

if __name__ == '__main__':
    app.run(debug=True)
