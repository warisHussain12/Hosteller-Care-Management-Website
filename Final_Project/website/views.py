from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user

from .models import Student, Proctor, Warden, Complaint, Message
from . import db

views = Blueprint("views", __name__)    

complaintIdforWarden = 0

@views.route("/")
@views.route("/loginHome")
def loginHome():
    return render_template("loginHome.html")

@views.route("/studentLogin")
def studentLogin():
    return render_template("./login/studentLogin.html")

@views.route("/proctorLogin")
def proctorLogin():
    return render_template("./login/proctorLogin.html")

@views.route("/wardenLogin")
def wardenLogin():
    return render_template("./login/wardenLogin.html")

@views.route("/studentHome")
@login_required
def studentHome():
    messages = Message.query.all()
    complaints = Complaint.query.all()
    return render_template("./home/studentHome.html", messages=messages, complaints=complaints, user=current_user)

@views.route("/proctorHome")
@login_required
def proctorHome():
    complaints = Complaint.query.all()
    return render_template("./home/proctorHome.html", complaints=complaints)

@views.route("/proctorPageMessageHistory")
@login_required
def proctorPageMessageHistory():
    messages = Message.query.all()
    complaints = Complaint.query.all()
    return render_template("./features/proctorPageMessageHistory.html", messages=messages, complaints=complaints, user=current_user)

@views.route("/studentPageMessageHistory")
@login_required
def studentPageMessageHistory():
    messages = Message.query.all()
    complaints = Complaint.query.all()
    return render_template("./features/studentPageMessageHistory.html", messages=messages, complaints=complaints, user=current_user)

@views.route("/forwardWarden/<complaintId>")
@login_required
def forwardWarden(complaintId):
    complaintIdforWarden = complaintId
    return redirect(url_for("views.proctorHome"))

@views.route("/wardenHome")
@login_required
def wardenHome():
    complaints = Complaint.query.all()
    return render_template("./home/wardenHome.html", complaints=complaints, user=current_user)

@views.route("/addStudent")
def addStudent():
    return render_template("addStudent.html")

@views.route("/addProctor")
def addProctor():
    return render_template("addProctor.html")

@views.route("/addWarden")
def addWarden():
    return render_template("addWarden.html")

@views.route("/deleteUser")
def deleteUser():
    return render_template("deleteUser.html")

# @views.route("/records")
# def records():
#     return render_template("./features/records.html")

@views.route("/raiseComplaint", methods=["GET", "POST"])
@login_required
def raiseComplaint():
    if request.method == "POST":
        text = request.form.get("complaint-text")

        if not text:
            flash("Post cannot be empty!", category='error')
        else:
            complaint = Complaint(text=text, author=current_user.id)
            db.session.add(complaint)
            db.session.commit()
            flash("Complaint successfully raised!", category='success')
            return redirect(url_for("views.studentHome"))
    return render_template("./features/raiseComplaint.html", user=current_user)

@views.route("/messageStudent/<complaintId>", methods=["GET", "POST"])
@login_required
def messageStudent(complaintId):
    if request.method == "POST":
        message = request.form.get("message-text")

        if not message:
            flash("Message cannot be empty!", category='error')
        else:
            message = Message(message=message, author=current_user.id, complaintId=complaintId)
            db.session.add(message)
            db.session.commit()
            flash("Message successfully sent!", category='success')
            return redirect(url_for("views.proctorHome"))
    return render_template("./features/messageStudent.html", user=current_user)