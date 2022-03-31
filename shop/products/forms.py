from email.policy import default
from xxlimited import Str
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form,IntegerField, StringField, DecimalField, TextAreaField, validators

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    quality = TextAreaField('Quality', [validators.DataRequired()])

    image_1 = FileField('Image 1',
     validators=[FileAllowed(['jpg','png','gif','jpeg'], 'images only please')])
    image_2 = FileField('Image 2',
     validators=[FileAllowed(['jpg','png','gif','jpeg'], 'images only please')])
    image_3 = FileField('Image 3',
     validators=[FileAllowed(['jpg','png','gif','jpeg'], 'images only please')])
    