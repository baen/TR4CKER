from flask import Flask, render_template, request, redirect, url_for, session
import db
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "gtg"


@app.route("/")
def index():
    return render_template("firstpg.html")

@app.route("/login", methods=["GET", "POST"])
def Login():
        
    if session.get('username') != None:
        return redirect("/")

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']


        user = db.CheckLogin(username, password)
        if user:

            session['id'] = user['id']
            session['username'] = user['username']

            return redirect("/")

    return render_template("login.html")

@app.route("/home")
def Home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def Register():
    
    if session.get('username') != None:
        return redirect("/")
    
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if db.RegisterUser(username, password):
            return redirect("/")

    return render_template("register.html")

@app.route("/list")
def ExerciseList():
    return render_template("list.html")

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

app.run(debug=True, port=5000)