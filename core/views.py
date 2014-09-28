from flask import Blueprint, render_template, abort, request, Response, redirect, url_for
from flask_login import login_user, login_required
from jinja2 import TemplateNotFound

from citations import getCitation

core_pages = Blueprint('core_page', __name__, template_folder="templates")


@core_pages.route("/")
@login_required
def menu():
    return render_template("menu.html")


@core_pages.route("/login", methods=["GET", "POST"])
def login():
    from users import Users
    if request.method == "POST":
        if not Users.authentification(str(request.form["username"]), str(request.form["password"])):
            return render_template("login.html", citation=getCitation(), message="Invalid credential.")
        else:
            print Users.get_by_pseudonyme(request.form["username"])
            # login_user(Users.get_by_pseudonyme(request.form["username"]))
            return redirect(request.args.get("next") or "/")
    else:


        return render_template("login.html", citation=getCitation())


@core_pages.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")
