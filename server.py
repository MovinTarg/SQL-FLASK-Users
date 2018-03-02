from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
app.secret_key = 'root'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
mysql = MySQLConnector(app,'users')

@app.route('/users')
def users():
    query = "SELECT * FROM users"
    users = mysql.query_db(query)
    return render_template('index.html', all_users = users)
#GET request - calls the index method to display all the users. This will need a template.

@app.route('/users/new')
def new_user():
    return render_template('new.html')
#GET request - calls the new method to display a form allowing users to create a new user. This will need a template.

@app.route('/users/<id>')
def show_user(id):
    query = "SELECT users.id, CONCAT(first_name, ' ', last_name) AS full_name, email, created_at FROM users WHERE users.id = :id"
    data = {
        'id': id
    }
    user = mysql.query_db(query, data)
    return render_template('view.html', user = user)
#GET - calls the show method to display the info for a particular user with given id. This will need a template.

@app.route('/users/<id>/edit')
def edit_user(id):
    query = "SELECT first_name, last_name, email FROM users WHERE users.id = :id"
    data = {
        'id': id
    }
    user = mysql.query_db(query, data)
    return render_template('edit.html', user = user)
#GET request - calls the edit method to display a form allowing users to edit an existing user with the given id. This will need a template.

@app.route('/users/create', methods=['POST'])
def create_user():
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }

    check = "SELECT email FROM users"
    
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    for i in (mysql.query_db(check)):
        if i['email'] == email:
            flash("Email already in database")
            return redirect('/')
    if len(email) < 1:
        flash("Email cannot be empty!")
        return redirect('/')
    elif not EMAIL_REGEX.match(email):
        flash("Invalid Email Address!")
        return redirect('/')
    elif len(first_name) < 1:
        flash("First name cannot be empty!")
        return redirect('/')
    elif any(i.isdigit() for i in first_name) == True:
        flash("Invalid first name!")
        return redirect('/')
    elif len(last_name) < 1:
        flash("Last name cannot be empty!")
        return redirect('/')
    elif any(i.isdigit() for i in last_name) == True:
        flash("Invalid last name!")
        return redirect('/')
    else:
        flash("Successfully Registered!")
        mysql.query_db(query, data)
        return redirect ('/users/<id>')
#POST - calls the create method to insert a new user record into our database. This POST should be sent from the form on the page /users/new. Have this redirect to /users/<id> once created.

@app.route('/users/<id>/destroy')
def delete_user(id):
    query = "DELETE FROM users WHERE id = :id"
    data = {
        'id': id
    }
    mysql.query_db(query, data)
    return redirect('/users')
#GET - calls the destroy method to remove a particular user with the given id. Have this redirect back to /users once deleted.

@app.route('/users/<id>', methods=['POST'])
def update_user(id):
    query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email, updated_at = NOW() WHERE id = :id"
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'id': id
    }

    check = "SELECT email FROM users"
    
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    for i in (mysql.query_db(check)):
        if i['email'] == email:
            flash("Email already in database")
            return redirect('/')
    if len(email) < 1:
        flash("Email cannot be empty!")
        return redirect('/')
    elif not EMAIL_REGEX.match(email):
        flash("Invalid Email Address!")
        return redirect('/')
    elif len(first_name) < 1:
        flash("First name cannot be empty!")
        return redirect('/')
    elif any(i.isdigit() for i in first_name) == True:
        flash("Invalid first name!")
        return redirect('/')
    elif len(last_name) < 1:
        flash("Last name cannot be empty!")
        return redirect('/')
    elif any(i.isdigit() for i in last_name) == True:
        flash("Invalid last name!")
        return redirect('/')
    else:
        flash("Successfully Updated!")
        mysql.query_db(query, data)
        return redirect ('/users/<id>')
#POST - calls the update method to process the submitted form sent from /users/<id>/edit. Have this redirect to /users/<id> once updated.

app.run(debug=True)