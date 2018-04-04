from mysqlconnection import MySQLConnector
from flask import Flask, request, redirect, render_template, session, flash
import re
import md5
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app, 'wall')


@app.route('/')
def index():
    users = mysql.query_db("SELECT * FROM users")
    return render_template('index.html', all_users=users)



@app.route('/wall')
def wall():
    messages = mysql.query_db("SELECT users.first_name, messages.* FROM users JOIN messages on messages.user_id=users.id")
    comments = mysql.query_db("SELECT * FROM comments")
    print messages
    return render_template('wall.html', all_messages=messages, all_comments=comments)



@app.route('/newuser', methods=['POST']) 
def newuser():

    print "----"
    session['first_name'] = request.form['first_name']
    last = request.form['last_name']
    email = request.form['email']
    password = md5.new(request.form['password']).hexdigest()

    print session['first_name']
    print last
    print email
    print password
    print "----"

    if len(session['first_name']) and len(last) < 2:
        flash("At least 2 characters for first and last names")
        if not EMAIL_REGEX.match(request.form['email']):
            flash("Email is not valid")

        if len(password) < 8:
            flash("Password must be over 8 characters")
    else:
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first, :last, :email, :password, NOW(), NOW())"

        data = {
            'first': session['first_name'],
            'last': last,
            'email': email,
            'password': password
            }
        
        mysql.query_db(query, data)
        flash("Thank you for submitting the form as all entires are correct")

    return redirect('/')



@app.route('/login', methods=['POST'])
def login():
    log_email = request.form['log_email']
    log_password = md5.new(request.form['log_password']).hexdigest()
    
    user_query = "SELECT * FROM users where users.email = :email AND users.password = :password"
    query_data = {
        'email': log_email,
        'password': log_password
        }
    user = mysql.query_db(user_query, query_data)

    if not EMAIL_REGEX.match(log_email):
            flash("Email Address to sign in is not valid")
            return redirect('/')

    if len(log_password) and len(log_email) < 1:
        flash("A password and email address is required for a login.")
        return redirect('/')

    if log_email == query_data['email']:
        flash("You have been signed in")
        print "Users: ", user_query
        print "query_data ", query_data
        print "email ", log_email
        # saved password
        print "password ", log_password
        return redirect('/wall')
    else:
        flash("The Email Address and/or password is incorrect")
        print "Users ", user
        print "query_data ", query_data
        print "email ", log_email
        # saved password
        print "password ", log_password
        return redirect('/')



@app.route('/post-message', methods=['POST'])
def message():
    post_message = request.form['textarea']
    print "Form Message:", post_message

    query = "INSERT INTO messages (message, created_at, updated_at) VALUES (:message, NOW(), NOW())"

    data = {
        'message' : post_message
        }
        
    mysql.query_db(query, data)
    
    return redirect('/wall')



@app.route('/post_comment', methods=['POST'])    
def comment():
    comment = request.form['comment']
    print "Comment:", comment

    query = "INSERT INTO comments (comment, created_at, updated_at) VALUES (:comment, NOW(), NOW())"

    data = {
        'comment' : comment
        }
        
    mysql.query_db(query, data)
    return redirect('/wall')


app.run(debug=True)