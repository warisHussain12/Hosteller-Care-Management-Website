from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    registrationId = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    complaints = db.relationship('Complaint', backref='student', passive_deletes=True)
    
    def __repr__(self):
        return f'<Student: {self.registrationId}-{self.password}>'
    
class Proctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    proctorId = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    messages = db.relationship('Message', backref='proctor', passive_deletes=True)
    
class Warden(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    wardenId = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    complaintDate = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    messages = db.relationship('Message', backref='complaint', passive_deletes=True)
    def __repr__(self):
        return f'<Complaint: {self.text}>'
    
# class toWardenComplaint(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text, nullable=False)
#     date_received = db.Column(db.DateTime(timezone=True), default=func.now())
#     author = db.Column(db.Integer, db.ForeignKey('student.id', ondelete="CASCADE"), nullable=False)
#     sentBy = db.Column(db.Integer, db.ForeignKey('proctor.id', ondelete="CASCADE"), nullable=False)
    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('proctor.id', ondelete="CASCADE"), nullable=False)
    complaintId = db.Column(db.Integer, db.ForeignKey('complaint.id', ondelete="CASCADE"), nullable=False)