import google.generativeai as genai
from flask import Flask , redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random
from flask_migrate import Migrate
from env.secret import api
from medico.programs import *
app = Flask(__name__)
app.config["SECRET_KEY"] ="dsojfksfvnvbnrdhslahjgvhbvh"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///patients.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)
app.app_context().push()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(10),  nullable = False)
    weight = db.Column(db.Integer, nullable = False)
    symptom = db.Column(db.String(500),  nullable = False)
    severity = db.Column(db.String(10),  nullable = False)
    token = db.Column(db.Integer,nullable = True,unique = True)
    
class Doctor(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String(200), nullable = False)

def gemResponse(prompt : str = None):
    genai.configure(api_key=api)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

@app.route("/",methods = ["GET","POST"])
def form():
    if request.method == "POST":
        name = request.form.get("patientname")
        age = request.form.get("patientage")
        weight = request.form.get("patientweight")
        gender = request.form.get("patientgender")
        symptom = request.form.get("patientsymptom")
        prompt = f"""Patient's age {age} years old, weight {weight} kg and gender {gender}.His/Her symtomps are {symptom}.
        Now provide severity of that patient in this three category: serious, moderate ,normal.must reply in one word."""
        print(request.form)
        severity = gemResponse(prompt).strip()
        new_patient = Patient(
            name = name,
            age = age,
            weight = weight,
            gender = gender,
            symptom = symptom,
            severity = severity,
            token = random.randint(1,10000)
        )
        if " " not in severity:
            db.session.add(new_patient)
            db.session.commit()
            return render_template("form.html")
        return render_template("form.html")

        
    return render_template("form.html")
@app.route("/patientList")
def patientList():
    patient = Patient.query.all()
    patients = prioritySort(patient)
    return render_template("patientList.html",patients = patients)
@app.route("/registration",methods = ["GET","POST"])
def registration():
    if request.method == "POST":
        data = request.form.to_dict()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        confirmPassword = data.get("confirmPassword")
        if password == confirmPassword:
            newDoctor = Doctor(
                name = name,
                email = email,
                password = password
            )
            db.session.add(newDoctor)
            db.session.commit()
            return "Account ctreated successfully"
        return redirect(url_for("registration"))
    return render_template("registration.html")
@app.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "POST":
        data = request.form.to_dict()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        info = Doctor.query.filter_by(email = email).first()
        if password == info.password:
            session['isDoctor'] = True
            return redirect(url_for("patientList"))
        return redirect(url_for('login'))
    return render_template("login.html")
@app.route("/action/<int:delNo>")
def action(delNo : int):
    donePatient = Patient.query.filter_by(token = delNo).first()
    if(donePatient == None):
        return redirect(url_for("patientList"))
    db.session.delete(donePatient)
    db.session.commit()
    return redirect(url_for("patientList"))
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug = True, port = 5001)