from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "xyz123Anonymous"
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    from .models import Student, Proctor, Warden, Complaint
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.proctorLogin"
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return Student.query.get(int(id))
    return app

def create_database(app):
    if not path.exists("website" + DB_NAME):
        db.create_all(app=app)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# @login_manager_student.user_loader
# def load_user(id):
#     if session['account_type'] == 'Student':
#         return Student.query.get(int(user_id))
#     elif session['account_type'] == 'Proctor':
#         return Proctor.query.get(int(user_id))
#     elif session['account_type'] == 'Warden':
#         return Warden.query.get(int(user_id))
# return app