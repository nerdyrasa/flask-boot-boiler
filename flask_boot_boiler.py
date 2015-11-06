from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Base, Category, CategoryItem, User

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def show_categories():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('index.html', categories=categories)


@app.route('/items/<int:category_id>')
def items(category_id):
    #category = session.query(Category).filter_by(category_id=category_id).one()
    print "show all the items"
    items=session.query(CategoryItem).filter_by(category_id=category_id)
    print 'items {}'.format(items)
    return render_template('items.html', items=items)


@app.route('/item/<int:item_id>')
def show_item(item_id):
    print "show item"
    item=session.query(CategoryItem).filter_by(id=item_id).one()
    print "item = {}".format(item)
    return render_template('details.html', item=item)


if __name__ == '__main__':
    app.run()
