from flask import Flask, render_template, request, redirect, url_for, session, flash
import db
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "gtg"

@app.route("/")
def index():
    if session.get('username') != None:
        return redirect("/home")
    
    return render_template("index.html")

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

    exercises = db.GetCurrentWorkout()
    
    return render_template("home.html", Exerciseslist=exercises)

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
        try:
            exercisename = request.form.get('exercisename')
            reps = request.form.get('reps')
            sets = request.form.get('sets')
            weight = request.form.get('weight', 0)
            rest_timer = request.form.get('rest_timer', 60)
            
            # Validate required fields
            if not all([exercisename, reps, sets, rest_timer]):
                flash('Please fill in all required fields.', 'error')
                return redirect("/list")
            
            # Convert to appropriate types
            reps = int(reps)
            sets = int(sets)
            weight = float(weight) if weight else 0
            rest_timer = int(rest_timer)
            
            if db.addExercises(exercisename, reps, sets, weight, rest_timer):
                flash('Exercise added successfully!', 'success')
            else:
                flash('Failed to add exercise.', 'error')
                
        except ValueError:
            flash('Please enter valid numbers for reps, sets, weight, and rest timer.', 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
        
        return redirect("/list")
    
    return render_template("list.html")

@app.route('/delete/<int:id>')
def delete_exercise(id):
    if session.get('username') == None:
        return redirect("/")
    
    # Use the database function
    db.DeleteExercise(id)
    return redirect('/home')

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)