from shutil import ExecError
from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app
from shop.products.models import Addproduct, Brand, Category

def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

def increase_quantity(sess_dict, new_dict, sess_id):
    sess_dict[sess_id]['quantity'] = str(int(sess_dict[sess_id]['quantity']) + int(new_dict[sess_id]['quantity']))
    return sess_dict


@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        quality = request.form.get('quality')
        product = Addproduct.query.filter_by(id=product_id).first()

        if product_id and quantity and quality and request.method=="POST":
            DictItems = {product_id:{
                            'name': product.name,
                            'price': product.price,
                            'discount':product.discount,
                            'quality': quality,
                            'quantity': quantity,
                            'image': product.image_1,
                            'qualities': product.quality}
                         }
            if 'Shoppingcart' in session:
                if product_id in session['Shoppingcart']:
                    session['Shoppingcart'] = increase_quantity(session["Shoppingcart"], DictItems, product_id)
                    print(session['Shoppingcart'])
                    print(f"The product {session['Shoppingcart'][product_id]['name']}'s quantity increased by {DictItems[product_id]['quantity']} in your cart.")
                    
                else:
                    session['Shoppingcart'] = MergeDicts(session["Shoppingcart"], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getCart():

    brands = Brand.query.join(Addproduct, (Brand.id==Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id==Addproduct.category_id)).all()

    print("HEREEEE")
    print(session)

    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (float(product['discount'])/100 * float(product['price']))
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax = ("%.2f" % (.06 * float(subtotal)))
        conv_fee = ("%.2f" % (.02 * float(subtotal)))
        grandtotal = float("%.2f" %(1.06 * float(subtotal)))

    return render_template('products/carts.html', 
    tax=tax, conv_fee=conv_fee, grandtotal=grandtotal,
    brands=brands, categories=categories)

@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    if request.method=="POST":
        quantity = request.form.get('quantity')
        quality = request.form.get('quality') 
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key)==code:
                    item['quantity'] = quantity
                    item['quality'] = quality
                    flash('Item is updated!', 'success') 
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                print(session['Shoppingcart'])
                return redirect(url_for('getCart'))
    
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))
