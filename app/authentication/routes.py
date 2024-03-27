from forms import UserForm, LoginUserForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint("auth", __name__, template_folder="auth_templates")

@auth.route("/signup", methods = ["GET", "POST"])
def signup():
    form = UserForm()

    try:
        if request.method == "POST" and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            print(first_name, last_name, email, password)

            user = User(first_name, last_name, email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a new account. Welcome {first_name} {last_name}, to the MIB Team, I mean the car dealership!", "auth-success")
            return redirect(url_for("site.homepage"))
    except:
        raise Exception("Sorry, invalid form data")

    return render_template("sign_up.html", form=form)

@auth.route("/signin", methods = ["GET", "POST"])
def signin():
    form = LoginUserForm()

    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                print("SUCESSFULL")
                flash("You are sucessfully logged in.")
                return redirect(url_for("site.userpage"))
            else:
                print("FAILED 1")
                flash("Access Denied from the Crash-site Actively Radioactive (C.A.R) Dealership")
                return redirect(url_for("auth.signin"))
    except:
        print("FAILED 2")
        raise Exception("Sorry, invalid form data")

    return render_template("sign_in.html", form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("site.homepage"))