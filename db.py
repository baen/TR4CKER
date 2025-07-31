import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():
    db = sqlite3.connect(".database/exerciselist.db")
    db.row_factory = sqlite3.Row
    return db

def RegisterUser(username, password):
    if username is None or password is None:
        return False

    try:
        db = GetDB()
        hash = generate_password_hash(password)
        db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, hash))
        db.commit()
        db.close()
        return True
    except Exception as e:
        print(f"Error registering user: {e}")
        return False

def CheckLogin(username, password):
    try:
        db = GetDB()
        user = db.execute("SELECT * FROM Users WHERE username=? COLLATE NOCASE", (username,)).fetchone()
        db.close()

        if user is not None:
            if check_password_hash(user['password'], password):
                return user
        return None
    except Exception as e:
        print(f"Error checking login: {e}")
        return None

def addExercises(exercisename, reps, sets, weight, rest_timer=60):
    if exercisename is None:
        return False
    
    try:

        reps = int(reps) if reps is not None else 0
        sets = int(sets) if sets is not None else 0
        weight = float(weight) if weight is not None and weight != '' else 0
        rest_timer = int(rest_timer) if rest_timer is not None else 60
        
        db = GetDB()
        db.execute("INSERT INTO Exerciseslist(exercisename, reps, sets, weight, rest_timer) VALUES (?, ?, ?, ?, ?)",
                   (exercisename, reps, sets, weight, rest_timer))
        db.commit()
        db.close()
        return True
    except Exception as e:
        print(f"Error adding exercise: {e}")
        return False

def GetCurrentWorkout():
    try:
        db = GetDB()
        currentworkout = db.execute("""SELECT id, exercisename, reps, sets, weight, rest_timer
                                 FROM Exerciseslist
                                 ORDER BY id DESC""").fetchall()
        db.close()
        return currentworkout
    except Exception as e:
        print(f"Error getting current workout: {e}")
        return []

def DeleteExercise(id):
    try:
        db = GetDB()
        db.execute('DELETE FROM Exerciseslist WHERE id = ?', (id,))
        db.commit()
        db.close()
        return True
    except Exception as e:
        print(f"Error deleting exercise: {e}")
        return False
    
def ClearAllExercises():
    try:
        db = GetDB()
        db.execute('DELETE FROM Exerciseslist')
        db.commit()
        db.close()
        return True
    
    except Exception as e:
        print(f"Error clearing all exercises: {e}")
        return False