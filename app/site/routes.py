from flask import Blueprint, render_template

site = Blueprint("site", __name__, template_folder="site_templates")

@site.route("/")
def homepage():
    return render_template("home.html")

@site.route("/userpage")
def userpage():
    return render_template("user.html")

site.route("/inventory")
def inventory():
    return render_template("inventory.html")