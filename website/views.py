from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from passlib.hash import sha256_crypt
from . import db
from website.forms import RegisterForm,ClassForm,LoginForm
from website.decorators import login_required,logout_required
from .models import users, carts, Callback, Classes, complate
from flask import Blueprint, render_template


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def index():
    classes = Classes.query.all()
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        message = request.form['message']

        # Form verilerini veritabanına kaydet
        new_callback = Callback(name=name, phone=phone, email=email, message=message)
        db.session.add(new_callback)
        db.session.commit()
        flash("Request A Call Back Succesfully Sent!","success")
        
        return redirect(url_for("views.index"))
        
    return render_template('index.html',classes = classes)
    

@views.route("/about")
def about():
    return render_template('about.html')

@views.route("/class")
def classes():
    result = Classes.query.all()
    
    if result:
        classes = Classes.query.all()
        
        return render_template("class.html",classes = classes)
    else:
        return render_template("class.html")


#Register
@views.route("/register",methods = ["GET","POST"])
@logout_required
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        
        new_user = users(name=name, email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Succesfully Registered!","success")
        
        return redirect(url_for("views.login"))
    else:
        return render_template("register.html",form=form)


#Login
@views.route("/login",methods = ["GET","POST"])
@logout_required
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        
        result = db.session.query(users).filter_by(username=username).first()
        if result:
            data = db.session.query(users).filter_by(username=username).first()
            real_password = data.password
            if sha256_crypt.verify(password_entered,real_password):
                flash("Succesfully Logged!","success")
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("views.index"))
            else:
                flash("Wrong password entered!","danger")
                return redirect(url_for("views.login"))
        else:
            flash("Wrong username entered!","danger")
            return redirect(url_for("views.login"))
        
        
    return render_template("login.html",form = form)

#Logout
@views.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("views.index"))

#Dashboard
@views.route("/dashboard")
@login_required
def dashboard():
    result = db.session.query(Classes).filter_by(admin=session["username"]).all()
    if result:
        classes = db.session.query(Classes).filter_by(admin=session["username"]).all()
        return render_template("dashboard.html",classes = classes)
    else:
        return render_template("dashboard.html")

#Addtocart
@views.route("/addtocart/<string:id>")
@login_required
def addtocart(id):
    class_data = db.session.query(Classes).filter_by(id=id).first()

    if class_data:
        cart1 = carts(
            id=class_data.id,
            centername=class_data.centername,
            coachname=class_data.coachname,
            phone=class_data.phone,
            location=class_data.location,
            price=class_data.price,
            admin=session["username"],
            owner=class_data.admin
        )
        db.session.add(cart1)
        db.session.commit()
        
        flash("Successfully added to cart!","success")
        return redirect(url_for("views.classes"))

    else:
        flash("You can't add this!","danger")
        return redirect(url_for("views.classes"))

#Buy Page
@views.route("/buy")
@login_required
def buy():
    return render_template("buy.html")

#Complated
@views.route("/complated")
@login_required
def complated():
    result = carts.query.filter_by(admin=session["username"]).all() 

    if result:
        
        cart_data = db.session.query(carts).filter(carts.admin == session["username"]).all()
        
        for row in cart_data:
            carts1 = complate(
            id=row.id,
            centername=row.centername,
            coachname=row.coachname,
            phone=row.phone,
            location=row.location,
            price=row.price,
            admin=row.admin,
            owner=row.owner
        )
        db.session.add(carts1)
        db.session.commit()
        
        flash("Payment Succesfully Complated!","success")
        return redirect(url_for("views.profile"))

    else:
        flash("Payment Failed!","danger")
        return redirect(url_for("views.cart"))

#Detail Coach Page
@views.route("/coach/<string:id>")
def coach(id):
    coachclass = db.session.query(Classes).filter_by(id=id).first()
    
    if coachclass:
        coachclass = db.session.query(Classes).filter_by(id=id).first()
        return render_template("coach.html",coachclass = coachclass)
    else:
        return render_template("coach.html")



#Add Class
@views.route("/addboxingcenter",methods = ["GET","POST"])
def addclass():
    form = ClassForm(request.form)
    if request.method == "POST" and form.validate():
        centername = form.centername.data
        coachname = form.coachname.data
        phone = form.phone.data
        location = form.location.data
        price = form.price.data
        aboutcoach = form.aboutcoach.data
        
        new_class = Classes(
            centername=centername,
            coachname=coachname,
            phone=phone,
            location=location,
            price=price,
            aboutcoach=aboutcoach,
            admin=session["username"]
        )
        db.session.add(new_class)
        db.session.commit()
        
        
        flash("Boxing Center Succesfully Added!","success")
        return redirect(url_for("views.dashboard"))
        
    return render_template("addboxingcenter.html",form = form)

#Class Delete
@views.route("/delete/<string:id>")
@login_required
def delete(id):
    class_to_delete = db.session.query(Classes).filter_by(admin=session["username"], id=id).first()
    
    if class_to_delete:
        db.session.delete(class_to_delete)
        db.session.commit()
        
        return redirect(url_for("views.dashboard"))
        
    else:
        flash("You can't delete this Boxing Center!","danger")
        return redirect(url_for("views.index"))
    
#Cart Delete
@views.route("/remove/<string:id>")
@login_required
def remove(id):
    id_condition = carts.id == id
    admin_condition = carts.admin == session["username"]
    item_to_remove = db.session.query(carts).filter(id_condition,admin_condition).first()
    
    if item_to_remove:
        db.session.delete(item_to_remove)
        db.session.commit()
        
        return redirect(url_for("views.cart"))
        
    else:
        flash("You can't remove this!","danger")
        return redirect(url_for("views.cart"))    
    
#Class Update
@views.route("/edit/<string:id>",methods = ["GET","POST"])
@login_required
def update(id):
    if request.method == "GET":
        class_to_update = db.session.query(Classes).filter_by(id=id, admin=session["username"]).first()
       
        if class_to_update == 0:
            flash("You can't this operation!","danger")
            return redirect(url_for("views.index"))
        else:
            form = ClassForm(obj=class_to_update)
            
            return render_template("update.html",form=form)
        
    else:
        #Post request
        form = ClassForm(request.form)
        class_to_update = db.session.query(Classes).filter_by(id=id, admin=session["username"]).first()
        
        class_to_update.centername = form.centername.data
        class_to_update.coachname = form.coachname.data
        class_to_update.phone = form.phone.data
        class_to_update.location = form.location.data
        class_to_update.price = form.price.data
        class_to_update.aboutcoach = form.aboutcoach.data
        
        db.session.commit()
        
        flash("Boxing Center Updated Successfully!","success")
        return redirect(url_for("views.dashboard"))
    
#Cart        
@views.route("/cart")
@login_required
def cart():
    classes = db.session.query(carts).filter_by(admin=session["username"]).all()
    
    if classes:
        toplamprice = sum(row.price for row in classes)
            
        return render_template("cart.html",classes = classes,toplamprice = toplamprice)
    else:
        return render_template("cart.html")
            
#Profile
@views.route("/profile")
@login_required
def profile():
    user = db.session.query(users).filter_by(username=session["username"]).first()
    
    if user:
        complatedorders = db.session.query(complate).filter_by(admin=session["username"]).all()
        owners = db.session.query(complate).filter_by(owner=session["username"]).all()
        return render_template("profile.html",complatedorders = complatedorders,user = user,owners = owners )
    else:
         return render_template("profile.html")
     

#Search URL
@views.route("/search",methods = ["GET","POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("views.index"))
    else:
        keyword = request.form.get("keyword")
        classes = db.session.query(Classes).filter(Classes.centername.like(f"%{keyword}%")).all()
        
        if classes == 0:
            flash("Doesn't find anything!","warning")
            return redirect(url_for("views.classes"))
        else:
            return render_template("class.html",classes = classes)
