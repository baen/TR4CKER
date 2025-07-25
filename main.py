from flask import Flask, render_template, request, redirect, url_for, session
import db
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "gtg"


@app.route("/")
def index():

    if session.get('username') != None:
        return redirect("/home")
    
    return render_template("firstpg.html")

@app.route("/login", methods=["GET", "POST"])
def Login():
        
    if session.get('username') != None:
        return redirect("/home")

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = db.CheckLogin(username, password)
        
        if user:

            session['id'] = user['id']
            session['username'] = user['username']

            return redirect("/home")

    return render_template("login.html")

@app.route("/home", methods=["GET", "POST"])
def Home():
    
    if session.get('username') == None:
        return redirect("/")

    conn = sqlite3.connect('.database/exerciselist.db')

    currentworkout = db.GetCurrentWorkout
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Exerciseslist')
    conn.close()

    return render_template("home.html", Exerciseslist=currentworkout())

@app.route("/register", methods=["GET", "POST"])
def Register():
    
    if session.get('username') != None:
        return redirect("/home")
    
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if db.RegisterUser(username, password):
            return redirect("/home")

    return render_template("register.html")

@app.route("/list", methods=["GET", "POST"])
def ExerciseList():
    
    if session.get('username') == None:
        return redirect("/")
    
    if request.method == "POST":
        exercisename = request.form['exercisename']
        reps = request.form['reps']
        sets = request.form['sets']
        weight = request.form['weight']

        db.addExercises(exercisename, reps, sets, weight)
    
    return render_template("list.html")

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

app.run(debug=True, port=5000)