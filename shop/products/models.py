from enum import unique
from shop import db
from datetime import datetime


class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    quality = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('categories', lazy=True))

    dist_id = db.Column(db.Integer, db.ForeignKey('dist.id'), nullable=True)
    dist = db.relationship('Dist', backref=db.backref('dists', lazy=True))
    

    image_1 = db.Column(db.String(150), nullable=False, default="image.jpg")
    image_2 = db.Column(db.String(150), nullable=False, default="image.jpg")
    image_3 = db.Column(db.String(150), nullable=False, default="image.jpg")

    #def __repr__(self):
    #    return '<Addproduct %r>' % self.title


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

class Dist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=False)
    fname = db.Column(db.String(30), nullable=False, unique=False)
    city = db.Column(db.String(30), nullable=False, unique=False)
    phone_number = db.Column(db.String(30), nullable=False, unique=True)
    aadhar_number = db.Column(db.String(30), nullable=False, unique=True)

db.create_all()