from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .import db
from .models import Student, Proctor, Warden, Complaint

auth = Blueprint("auth", __name__)

@auth.route("/studentLogin", methods=['GET', 'POST'])
def studentLogin():
    if request.method == 'POST':
        registrationId = request.form.get("registrationId")
        password = request.form.get("password")

        student = Student.query.filter_by(registrationId=registrationId).first()
        if student:
            if check_password_hash(student.password, password):
                flash("Logged In!", category='success')
                login_user(student, remember=True)
                return redirect(url_for('views.studentHome'))
            else:
                flash("Incorrect Password!", category='error')
        else:
            flash("User doesn't exist!", category='error')
    return render_template("./login/studentLogin.html", student=current_user)

@auth.route("/proctorLogin", methods=['GET', 'POST'])
def proctorLogin():
    if request.method == 'POST':
        proctorId = request.form.get("proctorId")
        password = request.form.get("password")

        proctor = Proctor.query.filter_by(proctorId=proctorId).first()
        if proctor:
            if check_password_hash(proctor.password, password):
                flash("Logged In!", category='success')
                login_user(proctor, remember=True)
                return redirect(url_for('views.proctorHome'))
            else:
                flash("Incorrect Password!", category='error')
        else:
            flash("User doesn't exist!", category='error')
    return render_template("./login/proctorLogin.html", proctor=current_user)

@auth.route("/wardenLogin", methods=['GET', 'POST'])
def wardenLogin():
    if request.method == 'POST':
        wardenId = request.form.get("wardenId")
        password = request.form.get("password")

        warden = Warden.query.filter_by(wardenId=wardenId).first()
        if warden:
            if check_password_hash(warden.password, password):
                flash("Logged In!", category='success')
                login_user(warden, remember=True)
                return redirect(url_for('views.wardenHome'))
            else:
                flash("Incorrect Password!", category='error')
        else:
            flash("User doesn't exist!", category='error')
    return render_template("./login/wardenLogin.html", warden=current_user)

@auth.route("/addStudent", methods=['GET', 'POST'])
def addStudent():
    if request.method == 'POST':
        registrationId = request.form.get("registrationId")
        if len(registrationId)>0:
            password = request.form.get("password")

            student_exists = Student.query.filter_by(registrationId=registrationId).first()
            if student_exists:
                flash('Student already exists!', category='error')
            else:
                new_student = Student(registrationId=registrationId, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_student)
                db.session.commit()
                login_user(new_student, remember=True)
                flash("Account created successfully!", category='success')
                return redirect(url_for('views.studentLogin'))
        return render_template("./login/studentLogin.html", user=current_user)
    return render_template("loginHome.html")

@auth.route("/addProctor", methods=['GET', 'POST'])
def addProctor():
    if request.method == 'POST':
        proctorId = request.form.get("proctorId")
        if len(proctorId)>0:
            password = request.form.get("password")

            proctor_exists = Proctor.query.filter_by(proctorId=proctorId).first()
            if proctor_exists:
                flash('Proctor already exists!', category='error')
            else:
                new_proctor = Proctor(proctorId=proctorId, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_proctor)
                db.session.commit()
                login_user(new_proctor, remember=True)
                flash("Account created successfully!", category='success')
                return redirect(url_for('views.proctorLogin'))
        return render_template("./login/proctorLogin.html", user=current_user)
    return render_template("loginHome.html")

@auth.route("/addWarden", methods=['GET', 'POST'])
def addWarden():
    if request.method == 'POST':
        wardenId = request.form.get("wardenId")
        if len(wardenId)>0:
            password = request.form.get("password")

            warden_exists = Warden.query.filter_by(wardenId=wardenId).first()
            if warden_exists:
                flash('Warden already exists!', category='error')
            else:
                new_warden = Warden(wardenId=wardenId, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_warden)
                db.session.commit()
                login_user(new_warden, remember=True)
                flash("Account created successfully!", category='success')
                return redirect(url_for('views.wardenLogin'))
        return render_template("./login/wardenLogin.html", user=current_user)
    return render_template("loginHome.html")

@auth.route("/deleteUser", methods=['GET', 'POST'])
def deleteUser():
    if request.method == 'POST':
        userId = request.form.get("userId")
        student = Student.query.filter_by(registrationId=userId).first()
        proctor = Proctor.query.filter_by(proctorId=userId).first()
        warden = Warden.query.filter_by(wardenId=userId).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            logout_user()
            flash("Account deleted successfully!", category='success')
            return redirect(url_for('views.loginHome'))
        elif proctor:
            db.session.delete(proctor)
            db.session.commit()
            logout_user()
            flash("Account deleted successfully!", category='success')
            return redirect(url_for('views.loginHome'))
        elif warden:
            db.session.delete(warden)
            db.session.commit()
            logout_user()
            flash("Account deleted successfully!", category='success')
            return redirect(url_for('views.loginHome'))
        else:
            flash("User doesn't exist!", category='error')
    return render_template("loginHome.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.loginHome"))