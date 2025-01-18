import google.generativeai as genai
from flask import Flask , redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import random
from flask_migrate import Migrate
from env.secret import api
app = Flask(__name__)

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
        severity = gemResponse(prompt)
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
            return "Patient data saved successfully with severity"
        return "Patient data not saved"
    
        
    return render_template("form.html")
@app.route("/queue")
def patientList():
    patient = Patient.query.all()
    seriousPatients = []
    moderatePatients = []
    normalPatients = []

    for i in patient:
        if i.severity.strip() == "Serious":
            seriousPatients.append(i)
        if i.severity.strip() == "Moderate":
            moderatePatients.append(i) 
        if i.severity.strip() == "Normal":
            normalPatients.append(i)
    
    # finalpatientList = seriousPatients + moderatePatients + normalPatients
    print(seriousPatients)
    seriousPatients.extend(moderatePatients)
    print(seriousPatients)
    seriousPatients.extend(normalPatients)
    for i in seriousPatients:

        print(i.severity,i.name)
    return render_template("queue.html",patients = seriousPatients)
if __name__ == "__main__":
    app.run(debug = True, port = 5001)