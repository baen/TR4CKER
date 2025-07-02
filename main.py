from flask import Flask, render_template, request, redirect, url_for, session
import db

app = Flask(__name__)
app.secret_key = "gtg"


@app.route("/")
def index():
    return render_template("firstpg.html")

@app.route("/login")
def Login():
    return render_template("login.html")

@app.route("/home")
def Home():
    return render_template("home.html")

@app.route("/register")
def Register():
    return render_template("register.html")

@app.route("/list")
def ExerciseList():
    return render_template("list.html")

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

app.run(debug=True, port=5000)