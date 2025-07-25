import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():

    db = sqlite3.connect(".database/exerciselist.db")
    db.row_factory = sqlite3.Row

    return db

def RegisterUser(username, password):

    if username is None or password is None:
        return False

    db = GetDB()
    hash = generate_password_hash(password)
    db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, hash,))
    db.commit()

    return True

def CheckLogin(username, password):

    db = GetDB()
    user = db.execute("SELECT * FROM Users WHERE username=? COLLATE NOCASE", (username,)).fetchone()

    if user is not None:
        if check_password_hash(user['password'], password):
            return user
        
    return None

def addExercises(exercisename, reps, sets, weight):

    if exercisename is None or reps is None or sets is None:
        return False
    
    db = GetDB()
    db.execute("INSERT INTO Exerciseslist(exercisename, reps, sets, weight) VALUES (?, ?, ?, ?)",
               (exercisename, reps, sets, weight))
    db.commit()

    return True

def GetCurrentWorkout():
    db = GetDB()
    currentworkout = db.execute("""SELECT Exerciseslist.exercisename, Exerciseslist.reps, Exerciseslist.sets,
                                    Exerciseslist.weight
                             FROM Exerciseslist
                             ORDER BY id DESC""").fetchall()
    db.close()
    return currentworkout