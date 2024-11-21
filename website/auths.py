from flask import Blueprint,render_template,url_for,request,redirect,flash,session
from .utilities.database import Database
import re

db = Database()

auth = Blueprint("auth",__name__)


@auth.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmpassword")
        email = request.form.get("email")
        if not email:
            flash("Please Enter An email.","info")
            return redirect(url_for("auth.signup"))
        if not re.fullmatch(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
            flash("Invalid Email","warning")
            return redirect(url_for("auth.signup"))
        if not username:
            flash("Please Enter A Username.","info")
            return redirect(url_for("auth.signup"))
        if db.userexists(username):
            flash("Username Taken Please Chose Another Username","info")
            return redirect(url_for("auth.signup"))
        if not password:
            flash("Please Enter A password.","info")
            return redirect(url_for("auth.signup"))
        if not confirm_password:
            flash("Please Enter A confirmed password.","info")
            return redirect(url_for("auth.signup"))
        if password != confirm_password:
            flash("Paswords Dont Match","warning")
            return redirect(url_for("auth.signup"))
        user = db.create_user(username,email,password)
        flash("Account Has Beeen Created","success")
        session["user_id"] = user.id
        session["username"] = user.name
        
        return redirect(url_for("view.index"))

    return render_template("signup.html")

@auth.route("/login", methods=["GET","POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    if request.method == "POST":
        if not email:
            flash("Please Enter An email.","info")
            return redirect(url_for("auth.login"))
        if not re.fullmatch(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
            flash("Invalid Email","warning")
            return redirect(url_for("auth.login"))
        if not username:
            flash("Please Enter A Username.","info")
            return redirect(url_for("auth.login"))
        if not password:
            flash("Please Enter A password.","info")
            return redirect(url_for("auth.login"))
        user = db.login(username,password,email) 
        if not user:
            flash("No User Found","info")
            return redirect(url_for("auth.login"))
        if user:
            session["user_id"] = user.id
            session["username"] = user.name
            flash("Logged In","success")
            return redirect(url_for("view.index"))
    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("view.index"))
