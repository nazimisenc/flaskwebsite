from flask import flash,redirect,url_for,session
from functools import wraps


#Kullanıcı Giriş Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Please login to view this page!","danger")
            return redirect(url_for("views.login"))

    return decorated_function

#Kullanıcı Çıkış Decorator
def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            flash("Please logout to view this page!","danger")
            return redirect(url_for("views.index"))
        else:
            return f(*args, **kwargs)
            

    return decorated_function