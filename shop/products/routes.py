from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from .models import Brand, Category, Dist, Addproduct
from .forms import Addproducts
import secrets, os

def brands():
    brands = Brand.query.join(Addproduct, (Brand.id==Addproduct.brand_id)).all()
    return brands

def categories():
    categories = Category.query.join(Addproduct, (Category.id==Addproduct.category_id)).all()
    return categories

def dists():
    dists = Dist.query.join(Addproduct, (Dist.id==Addproduct.dist_id)).all()
    return dists

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock>0).order_by(Addproduct.id.desc()).paginate(page=page, per_page=6)
    return render_template('products/index.html',
     products=products, brands=brands(), categories=categories())

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html', product=product,
     brands=brands(), categories=categories())

@app.route('/brand/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = Addproduct.query.filter_by(brand_id=id).paginate(page=page, per_page=6)
    
    return render_template('products/index.html', brand=brand, get_b=get_b,
     brands=brands(), categories=categories())

@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=6)
    
    return render_template('products/index.html', get_cat_prod=get_cat_prod, get_cat=get_cat,
     brands=brands(), categories=categories())

@app.route('/dist/<int:id>')
def get_dist(id):
    page = request.args.get('page', 1, type=int)
    get_dist = Category.query.filter_by(id=id).first_or_404()
    get_dist_prod = Addproduct.query.filter_by(category=get_dist).paginate(page=page, per_page=6)
    
    return render_template('products/index.html', get_dist_prod=get_dist_prod, get_dist=get_dist,
     brands=brands(), categories=categories())

     

@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = str(request.form.get('brand'))
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand "{getbrand}" was added to your database.', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))

    return render_template('products/addbrand.html', brands='brands')

@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))

    if request.method == "POST":
        getbrand = str(request.form.get('category'))
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The Category "{getbrand}" was added to your database.', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))

    return render_template('products/addbrand.html', categories='categories')

@app.route('/adddist', methods=['GET', 'POST'])
def adddist():
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))

    if request.method == "POST":
        getname = str(request.form.get('dist'))
        getcity = str(request.form.get('city'))
        getphno = str(request.form.get('phno'))
        cat = Dist(name=getname, city=getcity, phone_number=getphno)
        db.session.add(cat)
        flash(f'The Distributor "{getname}" was added to your database.', 'success')
        db.session.commit()
        return redirect(url_for('adddist'))

    return render_template('products/addbrand.html')

@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))

    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method=='POST':
        updatebrand.name = brand
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html',
     title='Update Brand Page', updatebrand=updatebrand)

@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash("Please login first", "danger")

    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method=="POST":
        updatecat.name = category
        flash(f'Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html',
     title='Update Category Page',
     updatecat=updatecat)

@app.route('/updatedist/<int:id>', methods=['GET', 'POST'])
def updatedist(id):
    if 'email' not in session:
        flash("Please login first", "danger")

    updatedist = Dist.query.get_or_404(id)
    dist = request.form.get('dist')
    city = request.form.get('city')
    phno = request.form.get('phno')
    if request.method=="POST":
        updatedist.name = dist
        updatedist.city = city
        updatedist.phone_number = phno
        flash(f'Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('dist'))
    return render_template('products/updatebrand.html',
     title='Update Distributor Page',
     updatedist=updatedist)

@app.route('/deletebrand/<int:id>', methods=["POST"])
def deletebrand(id):
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))

    brand = Brand.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} is deleted!', 'success')
        return redirect(url_for('admin'))
    flash(f'The brand {brand.name} cannot be deleted!', 'warning')
    return redirect(url_for('admin'))

@app.route('/deletecat/<int:id>', methods=["POST"])
def deletecat(id):
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))

    category = Category.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} is deleted!', 'success')
        return redirect(url_for('admin'))
    flash(f'The category {category.name} cannot be deleted!', 'warning')
    return redirect(url_for('admin'))

@app.route('/deletedist/<int:id>', methods=["POST"])
def deletedist(id):
    if 'email' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))

    dist = Dist.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(dist)
        db.session.commit()
        flash(f'The distributor {dist.name} is deleted!', 'success')
        return redirect(url_for('admin'))
    flash(f'The distributor {dist.name} cannot be deleted!', 'warning')
    return redirect(url_for('admin'))



@app.route('/addproduct', methods=["GET", "POST"])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    brands = Brand.query.all()
    categories = Category.query.all()
    dists = Dist.query.all()
    form = Addproducts(request.form)
    if request.method=="POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        quality = form.quality.data
        desc = form.description.data

        brand = request.form.get('brand')
        category = request.form.get('category')
        dist = request.form.get('dist')

        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+'.')
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+'.')
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+'.')
        
        addpro = Addproduct(name=name, price=price, discount=discount,
         stock=stock, desc=desc, quality=quality,
          brand_id=brand, category_id=category, dist_id=dist,
          image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database', 'success')
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('products/addproduct.html',
     title="Add Product page", form=form,
      brands=brands, categories=categories, dists=dists)

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    
    brand = request.form.get('brand')
    category = request.form.get('category')
    
    form = Addproducts(request.form)
    if request.method=="POST":
        product.name = form.name.data
        product.price = form.price.data
        product.desc = form.description.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.quality = form.quality.data

        product.brand_id = brand
        product.category_id = category

        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/'+product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+'.')
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+'.')

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/'+product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+'.')
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+'.')

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/'+product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+'.')
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+'.')
        
        db.session.commit()
        flash(f'Your product has been updated', 'success')
        return redirect(url_for('admin'))
    
    form.name.data = product.name
    form.price.data = product.price
    form.description.data = product.desc
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.quality.data = product.quality

    return render_template('products/updateproduct.html',
     form=form, brands=brands,
      categories=categories, product=product)

@app.route('/deleteproduct/<int:id>', methods=["POST"])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method=="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/images/'+product.image_1))
            os.unlink(os.path.join(current_app.root_path, 'static/images/'+product.image_2))
            os.unlink(os.path.join(current_app.root_path, 'static/images/'+product.image_3))
            
        except Exception as e:
            print(e)
            
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} has been removed.', 'success')
        return redirect(url_for('admin'))
    
    flash(f'Product cannot be removed.', 'danger')
    return redirect(url_for('admin'))
