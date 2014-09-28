from flask import Blueprint, render_template, abort
from flask_login import login_user, login_required
from jinja2 import TemplateNotFound

core_pages = Blueprint('core_page', __name__, template_folder="templates")

@core_pages.route("/")
@login_required
def base():
     return render_template("menu.html")

@core_pages.route("/login")
def login():
    return render_template("login.html")

@core_pages.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")