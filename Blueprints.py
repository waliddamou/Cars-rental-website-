import random

from flask import Blueprint , render_template, request, current_app, flash, redirect, url_for,send_file,send_from_directory,Response,jsonify
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
import uuid
from .models import Userr, db, Car
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import json
import datetime


Blueprints=Blueprint('Blueprints',__name__,template_folder='templates',static_folder='static')
UPLOAD_FOLDER = 'static/Uploaded_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
Bcrypt=Bcrypt()

@Blueprints.route('/',methods=['GET','POST'])
def index():
    cars=Car.query.all()[:3]
    return render_template("index.html",cars=cars)


@Blueprints.route('/OurCars',methods=['GET','POST'])
def OurCars():
    cars=Car.query.all()
    return render_template("OurCars.html",cars=cars)

@Blueprints.route('/ViewCar/<int:id>',methods=['GET','POST'])
def ViewCar(id):
    cars=Car.query.filter_by(id=id).first()
    return render_template("ViewCar.html",cars=cars)

@Blueprints.route('/Dashboared/EditCar/<int:id>',methods=['GET','POST'])
def EditCar(id):
    
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))
    cars=Car.query.filter_by(id=id).first()
    photo_list=''
    if request.method =="POST":
        cars.Name = request.form["name"]
        cars.marque = request.form["marque"]
        cars.modele = request.form["modele"]
        cars.version =  request.form["version"]
        cars.kilo = request.form["kilo"] 
        cars.energie = request.form["energie"]
        cars.boite = request.form["boite"]
        cars.description = request.form["description"]
        files = request.files.getlist("file")
        for i in files:
            photo_list=photo_list+i.filename+','
            i.save(os.path.join(UPLOAD_FOLDER, i.filename))    
        cars.Photos=photo_list
        db.session.add(new_car)
        db.session.commit()
        flash(f'La voiture a été Modifier',"warning")
    return render_template("EditCar.html",cars=cars)



@Blueprints.route('/About',methods=['GET','POST'])
def About():
    return render_template("about.html")

@Blueprints.route('/ContactUs',methods=['GET','POST'])
def ContactUs():
    return render_template("contact.html")



@Blueprints.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.Dashboard'))
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        userr=Userr.query.filter_by(Mail=email).first()
        if userr and Bcrypt.check_password_hash(userr.Password, password):
            login_user(userr)
            return redirect(url_for('.Dashboard'))
        else:
            flash(f"L'email ou le mot de passe est incorrect", "danger")
            return redirect(url_for('.login'))
    return render_template("login.html")

@Blueprints.route('/Dashboard',methods=['GET','POST'])
@login_required
def Dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))

    cars=Car.query.all()
    users=Userr.query.all()
    visits=random.randint(300, 1000)
    return render_template("Dashboard.html",cars=len(cars),users=len(users),visits=visits)


@Blueprints.route('/Dashboard/AddCar',methods=['GET','POST'])
@login_required
def AddCar():

    if not current_user.is_authenticated:
        return redirect(url_for('.login'))

    photo_list=''
    if request.method =="POST":
        Name = request.form["name"]
        marque = request.form["marque"]
        modele = request.form["modele"]
        version =  request.form["version"]
        kilo = request.form["kilo"] 
        energie = request.form["energie"]
        boite = request.form["boite"]
        description = request.form["description"]
        files = request.files.getlist("file")
        for i in files:
            photo_list=photo_list+i.filename+','
            i.save(os.path.join(UPLOAD_FOLDER, i.filename))    
        new_car=Car(Name=Name,Marque=marque,Modele=modele,Version=version,Kilo=kilo,Energie=energie,Boite=boite,Description=description,Photos=photo_list)
        db.session.add(new_car)
        db.session.commit()
        flash(f'La voiture a été ajouté',"success")
    return render_template("AddCar.html")


@Blueprints.route('/Dashboard/AllCars',methods=['GET','POST'])
@login_required
def AllCars():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))
    cars=Car.query.all()
    return render_template("AllCars.html",cars=cars)

@Blueprints.route('/Dashboard/AllUsers',methods=['GET','POST'])
@login_required
def AllUsers():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))
    users=Userr.query.all()
    return render_template("AllUsers.html",users=users)

@Blueprints.route('/Dashboard/EditUser/<int:id>',methods=['GET', 'POST'])
@login_required
def EditUser(id):
    if not current_user.is_authenticated:
        return redirect(url_for('.Connexion'))
    users=Userr.query.filter_by(id=id).first_or_404()
    if request.method == 'POST':
        First_name=request.form["firstname"]
        Last_name=request.form["lastname"]
        Email=request.form["email"]
        Password=request.form["password"].encode('utf-8')
        Phone=request.form["telephone"]
        Role=request.form["role"]
        salt=bcrypt.gensalt()
        hashed = bcrypt.hashpw(Password, salt)
        if request.files:
            photo=request.files['photo']
            if photo.filename == '':
                users.FirstName=First_name
                users.LastName=Last_name
                users.Mail=Email
                users.Password=hashed
                users.Phone=Phone
                users.Role=Role
                db.session.add(users)
                db.session.commit()
                flash(f"L'utilisateur a été Modifié ", "warning")
                return redirect(url_for('.ManageUsers'))
                
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(UPLOAD_FOLDER, filename))
                users.FirstName=First_name
                users.LastName=Last_name
                users.Mail=Email
                users.Password=hashed
                users.Phone=Phone
                users.Role=Role
                users.Photo=filename
                db.session.add(users)
                db.session.commit()
                flash(f"L'utilisateur a été Modifié ", "warning")
                return redirect(url_for('.AllUsers'))
    

    return render_template('EditUser.html',users=users)

@Blueprints.route('/Dashboard/DeleteUser/<int:id>',methods=['GET', 'POST'])
@login_required
def DeleteUser(id):
    if not current_user.is_authenticated:
        return redirect(url_for('.Connexion'))
    users=Userr.query.filter_by(id=id).first_or_404()
    if request.method=="POST":
        db.session.delete(users)
        db.session.commit()
        flash(f"l'utilisateur' a été supprimer",'warning')
        return redirect(url_for('.AllUsers'))

    

    return render_template('DeleteUser.html',users=users)

@Blueprints.route('/Dashboard/DeleteCar/<int:id>',methods=['GET', 'POST'])
@login_required
def DeleteCar(id):
    if not current_user.is_authenticated:
        return redirect(url_for('.Connexion'))
    users=Car.query.filter_by(id=id).first_or_404()
    if request.method=="POST":
        db.session.delete(users)
        db.session.commit()
        flash(f"l'utilisateur' a été supprimer",'warning')
        return redirect(url_for('.AllUsers'))

    

    return render_template('DeleteCar.html',users=users)

@Blueprints.route('/Dashboard/AddUser',methods=['GET','POST'])
@login_required
def AddUser():
    if not current_user.is_authenticated:
        return redirect(url_for('.login'))

    users=Userr.query.all()
    if request.method == 'POST':
        First_name=request.form["firstname"]
        Last_name=request.form["lastname"]
        Email=request.form["email"]
        for i in users:
            if i.Mail==Email:
                flash(f"l'email éxiste déja dans la Base de Donnée veuillez reessayer!",'warning')
                return redirect(url_for('.AddUser'))
        Password=request.form["password"].encode('utf-8')
        Phone=request.form["telephone"]
        Role=request.form["role"]
        salt=bcrypt.gensalt()
        hashed = bcrypt.hashpw(Password, salt)
        if request.files:
            photo=request.files['photo']
            if photo.filename == '':
                user=Userr(FirstName=First_name, LastName=Last_name, Mail=Email, Password=hashed, Phone=Phone)
                db.session.add(user)
                db.session.commit()
                flash(f"L'utilisateur a été Ajouté ", "success")
                return redirect(url_for('.AddUser'))
                
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(UPLOAD_FOLDER, filename))
                user=Userr(FirstName=First_name, LastName=Last_name, Mail=Email, Password=hashed, Phone=Phone,Photo=filename)
                db.session.add(user)
                db.session.commit()
                flash(f"L'utilisateur a été Ajouté ", "success")
                return redirect(url_for('.AddUser'))
    
    return render_template("AddUser.html")


@Blueprints.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))  