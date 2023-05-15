from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField
from wtforms.validators import DataRequired
from flask_pymongo import PyMongo
import confidential

app=Flask(__name__)
app.config['SECRET_KEY']=confidential.SECRET_KEY
app.config['MONGO_URI']=confidential.MONGO_URI
mongo=PyMongo(app)

class StudentForm(FlaskForm):
    name=StringField("Name: ",validators=[DataRequired()])
    age=IntegerField("Age: ",validators=[DataRequired()])
    submit=SubmitField("Add")

class StaffForm(FlaskForm):
    name=StringField("Name: ",validators=[DataRequired()])
    subject=StringField("Subject: ",validators=[DataRequired()])
    submit=SubmitField("Add")

student_collection=mongo.db.student_details
staff_collection=mongo.db.staff_details

@app.route('/',methods=["POST","GET"])
def index():
    students=student_collection.find()
    staffs=staff_collection.find()

    studForm=StudentForm()
    stafForm=StaffForm()
    if studForm.validate_on_submit():
        student_collection.insert_one({"name":studForm.name.data,"age":studForm.age.data})
        return redirect(url_for('index'))
    if stafForm.validate_on_submit():
        staff_collection.insert_one({"name":stafForm.name.data,"subject":stafForm.subject.data})
        return redirect(url_for('index'))
    return render_template("index.html",StudForm=studForm,StafForm=stafForm,Students=students,Staffs=staffs)

@app.route('/delete/student/<name>')
def studdelete(name):
    student_collection.delete_one({"name":name})
    return redirect(url_for('index'))

@app.route('/delete/staff/<name>')
def stafdelete(name):
    staff_collection.delete_one({"name":name})
    return redirect(url_for('index'))

@app.route('/update/student/<name>',methods=["POST","GET"])
def studupdate(name):
    studForm=StudentForm()
    student=student_collection.find_one({"name":name})
    if studForm.validate_on_submit():
        student_collection.replace_one({"name":name},{"name":studForm.name.data,"age":studForm.age.data})
        return redirect(url_for("index"))
    studForm.name.data=student['name']
    studForm.age.data=student["age"]
    return render_template('student_form.html',StudForm=studForm)

@app.route('/update/staff/<name>',methods=["POST","GET"])
def stafupdate(name):
    stafForm=StaffForm()
    staff=staff_collection.find_one({"name":name})
    if stafForm.validate_on_submit():
        staff_collection.replace_one({"name":name},{"name":stafForm.name.data,"subject":stafForm.subject.data})
        return redirect(url_for("index"))
    stafForm.name.data=staff['name']
    stafForm.subject.data=staff["subject"]
    return render_template('staff_form.html',StafForm=stafForm)

if __name__=="__main__":
    app.run(debug=True)