from flask import Flask, render_template
import db

app = Flask(__name__)
app.secret_key = "gtg"

@app.route("/")
def Intermediary():
    return render_template("firstpg.html")

@app.route("/home")
def Home():
    return render_template("home.html")

app.run(debug=True, port=5000)