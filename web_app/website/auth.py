# Store standard roots for our server
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, Request
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Just like views, we define a blueprint and both of these will have different URLs
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':        
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True) # remembers that user is logged in
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash("User does not exist.", category='error')
        

    return render_template("login.html", user=current_user)  # You can pass variables to the template here

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/create-user', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('userName')
        phy_cfgs = [ int(cfg.strip()) for cfg in request.form.get('phyCfgs').split(',')]
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        # TODO: Release date
        release_date = None

        user = User.query.filter_by(username=username).first()
        print("user = ", user)
        if user:
            flash('User already exists.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 3 character.', category='error')
        elif password1 != password2:
            flash('Password not matching', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='sha256'), phy_cfgs=phy_cfgs, release_date=release_date)
            db.session.add(new_user)   
            db.session.commit()            
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            # return a redirect to the URL for the home page
            #   views - bluprint name
            #   home - function name that you want to go to
            return redirect(url_for('views.home', user=current_user))

        
    return render_template("sign_up.html", user=current_user)
    
# When you render HTML you call it a template because there's a special templating language you can use with flask called Jinja which allows you to write some python in your HTML

@auth.route('/delete-user=<id>', methods=['DELETE'])
@login_required
def delete_user(id):
    user = User.query.filter_by(id=id).all()
    print(user)
    if user:
        # Remove User Requests
        all_requests = Request.query.filter_by(user_id=id).all()
        print(len(all_requests))
        print(all_requests)
        
        # if all_requests:
        #     for request in all_requests:
        #         db.session.delete(request)
        #     db.session.commit()
        
        # # remove user
        # db.session.delete(user)
        # db.session.commit()
    else:
        print("User doesn't exist") # TODO: replace with idk, 404 or something
    
    print(current_user.id)
    if user == current_user:
        print("-- CURRENT USER --")
    
    return jsonify({})

@auth.route('/clear-user-requests=<id>', methods=['DELETE'])
# @login_required
def clear_user_requests(id):
    # Remove User Requests
    all_requests = Request.query.filter_by(user_id=id).all()
    print(len(all_requests))
    print(all_requests)
    
    if all_requests:
        for request in all_requests:
            db.session.delete(request)
        db.session.commit()
    
    # return redirect(url_for('views.home', user=current_user))
    return jsonify({})


# Admin User


