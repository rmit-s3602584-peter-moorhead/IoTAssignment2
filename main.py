#main file
from flask import Flask, render_template, request, url_for, session, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import sys

app = Flask(__name__)


# Didn't work without secret key, didn't matter what it is
app.secret_key = 'your secret key'

#create table if not exists Person (
#                    PersonID int not null auto_increment,
#                    Name text not null,
#                    constraint PK_Person primary key (PersonID)
#                )"""
#
#ursor.execute("""
#                   CREATE TABLE IF NOT EXISTS `accounts` (
#                   `id` int(11) NOT NULL AUTO_INCREMENT,
#                   `username` varchar(50) NOT NULL,
#                   `password` varchar(255) NOT NULL,
#                   `email` varchar(100) NOT NULL,
#                   PRIMARY KEY (`id`)
#                   )""")

app.config['MYSQL_HOST'] = '35.244.72.137'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'Peopl'


mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    """
    This POST function gets the username and password from a html
    form and uses it to query the sql database.
    If the user exists in the database it opens a session on the server.
    If the user doesn't exist it messages the user that they incorrectly
    input their details or they aren't registered in the database.
    """
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['typeOfUser'] = account['typeOfUser']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
        
    return render_template('index.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    """
    Logout function to end the session and redirects to the login page
    """
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('typeOfUser', None)
   
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This function registers a new user. It first checks if the form data
    from the user already exists in the database via a POST request to
    the google sql database. The data is then processed through validation
    so that the data will be valid and can be created in the database.
    Once the form is correctly filled with valid data it will send it off
    to the database and a new user will be registered.
    """
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'firstName' in request.form and 'lastName' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        customer = "Customer"
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not firstName or not lastName:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s)', (username, password, firstName, lastName, email, customer,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    """
    This function checks that the user is logged in to a valid user
    and renders the individuals homepage. If its and admin user
    it will have extra features available.
    If its not logged in then the user will be redirected to the
    login page.
    """
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        if session['typeOfUser'] == 'Customer':
            return render_template('home.html', username=session['username'])
        else:
            return render_template('adminHome.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    """
    This function defines the route to the users profile page where
    they will be able to check their booking history.
    """
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        user = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', user=user)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/cars')
def cars():
    """
    This function will render the template for the cars available to
    hire. It also you can also search for available cars based on
    their attributes via a POST form in carQuery.
    """
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        #available = ''
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cars')
        #cursor.execute('SELECT * FROM cars WHERE bookedBy = %s', (available,))
        #cursor.execute('SELECT * FROM cars WHERE make = "Ford Falcon"')
        cars = cursor.fetchall()
        # Show the profile page with account info
        return render_template('cars.html', cars=cars)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/carManagement')
def carManagement():
    """
    An admin function that will let admin's perform database operations
    that regular users should not be able to.
    """
    if 'loggedin' in session:
        # User is loggedin show them the home page
        if session['typeOfUser'] == 'Customer':
            return redirect(url_for('login'))
        else:
            return render_template('carManagement.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/carQuery', methods=['GET', 'POST'])
def carQuery():
    
    """
    This function takes the data from a form and builds an sql query based
    on what variation of attribute user was looking for.
    If the form is blank it returns all the cars available like the cars route.
    It is probably susceptible to an SQL injection at the moment but will
    hopefully in the future provide a more robust input validation scheme.
    """
    
    if 'loggedin' in session:
        
        if request.method == 'GET':
            
            idCar = request.form['id']
            cursor.execute('SELECT * FROM cars')
            cars = cursor.fetchone()
            #print(cars)
            #return render_template('cars.html', cars=cars)
            return render_template('home.html')
        else:
            
            
            idcar = request.form['idCar']
            make = request.form['make']
            bodyType = request.form['bodyType']
            colour = request.form['colour']
            seats = request.form['seats']
            location = request.form['location']
            cost = request.form['cost']
            #bookedBy = 'Cathy'
            bookedBy = request.form['bookedBy']
            returned = 0

            sqlExpression = 'SELECT * FROM cars'
            count = 0
            
            if idcar == '' and make == '' and bodyType == '' and colour == '' and seats == '' and location == '' and cost == '' and bookedBy == '':
                return redirect(url_for('cars'))
            else:
                sqlExpression = 'SELECT * FROM cars WHERE '
                if idcar != '':
                    if count != 0:
                        sqlExpression = sqlExpression + ' AND ' + ' id = ' + idcar
                    else:
                        sqlExpression = sqlExpression + ' id = ' + idcar
                        count = 1
                        app.logger.info(count)

                if make != '':
                    if count != 0:
                        sqlExpression = sqlExpression + ' AND ' + ' make = ' + '"' + make + '"'
                    else:
                        sqlExpression = sqlExpression + ' make = ' + '"' + make + '"'
                        count += 1
                        app.logger.info(count)
                        
                if bodyType != '':
                    if count != 0:
                        sqlExpression = sqlExpression + ' AND ' + ' bodyType = ' + '"' + bodyType + '"'
                    else:
                        sqlExpression = sqlExpression + ' bodyType = ' + '"' + bodyType + '"'
                        count = 1
                        app.logger.info(count)
                        
                if colour != '':
                    if count != 0:
                        sqlExpression = sqlExpression + ' AND ' + ' colour = ' + '"' + colour + '"'
                    else:
                        sqlExpression = sqlExpression + ' colour = ' + '"' + colour + '"'
                        count = 1
                        app.logger.info(count)
                        
                if seats != '':
                    if count != 0:
                        sqlExpression = sqlExpression + ' AND ' + ' seats = ' + '"' + seats + '"'
                    else:
                        sqlExpression = sqlExpression + ' seats = ' + '"' + seats + '"'
                        count = 1
                        app.logger.info(count)
                        
                if location != '':
                    if count != 0:
                        sqlExpression = sqlExpression + ' AND ' + ' location = ' + '"' + location + '"'
                    else:
                        sqlExpression = sqlExpression + ' location = ' + '"' + location + '"'
                        count = 1
                        app.logger.info(count)
                        
                if cost != '':
                    if count != 0:
                        sqlExpression = sqlExpression + ' AND ' + ' cost = ' + '"' + cost + '"'
                    else:
                        sqlExpression = sqlExpression + ' cost = ' + '"' + cost + '"'
                        count = 1
                        app.logger.info(count)
                        
                if bookedBy != '':
                    if count != 0:
                        sqlExpression = sqlExpression + ' AND ' + ' bookedBy = ' + '"' + bookedBy + '"'
                    else:
                        sqlExpression = sqlExpression + ' bookedBy = ' + '"' + bookedBy + '"'
                        count = 1
                        app.logger.info(count)
                        
                app.logger.info(sqlExpression)
                
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                #cursor.execute('SELECT * FROM cars WHERE id = s% AND make = s% AND bodyType = s% AND colour = s% AND seats = s% AND location = s% AND cost = s% AND bookedBy = s%', (idcar, make, bodyType, colour, seats, location, cost, bookedBy,))
                #cursor.execute('SELECT * FROM cars WHERE id = %s OR make = %s OR bodyType = %s OR colour = %s OR seats = %s OR location = %s OR cost = %s OR bookedBy = %s OR returned = %s', (idcar, make, bodyType, colour, seats, location, cost, bookedBy, returned,))
                
                #cursor.execute('SELECT * FROM cars WHERE id = %s OR make = %s OR bodyType = %s OR colour = %s OR seats = %s OR location = %s OR cost = %s', (idcar, make, bodyType, colour, seats, location, cost,))
                #cursor.execute('SELECT * FROM cars WHERE id = %s AND make = %s AND bodyType = %s AND colour = %s AND seats = %s AND location = %s AND cost = %s', (idcar, make, bodyType, colour, seats, location, cost,))
                cursor.execute(sqlExpression)
                #cursor.execute('SELECT * FROM cars WHERE  bodyType = "Sedan"')

                #return redirect(url_for('cars'))
                cars = cursor.fetchall()
                # Show the profile page with account info
                return render_template('cars.html', cars=cars)
            
        
    return redirect(url_for('login'))


@app.route('/carBooking', methods=['GET', 'POST'])
def carBooking():
    
    """
    User will book a car by posting to the booking and car tables
    """
    if 'loggedin' in session:
        if request.method == 'POST':
            username = session['username']
            bookingCarId = request.form['bookingCarId']
            
            sqlExpression = 'UPDATE cars SET bookedBy = ' + '"' + username + '"' + ' WHERE id = ' + bookingCarId
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #cursor.execute(sqlExpression)
            #cursor.execute('UPDATE cars SET bookedBy = "Test" WHERE id = 4')
            cursor.execute('UPDATE cars SET bookedBy = %s WHERE id = %s', (username, bookingCarId,))
            #UPDATE cars SET bookedBy = "Test" WHERE id = 1
            
            app.logger.info(sqlExpression)
            
            return render_template('cars.html')
        else:
            return render_template('profile.html')
        
    else:
        return redirect(url_for('login'))
        
@app.route('/userhistory', methods=['POST'])
def userHistory():
    
    """
    User will display history of bookings
    """
    if 'loggedin' in session:
        if request.method == 'POST':
            id = session['id']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM bookings WHERE id = %d', (id,))
            history = cursor.fetchall()
            
            return render_template('userhistory.html', history=history)
        else:
            return render_template('profile.html')
        
    else:
        return redirect(url_for('login'))
    
    
    

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')