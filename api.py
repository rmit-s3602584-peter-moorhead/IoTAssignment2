#main file
from flask import Flask, render_template, request, url_for, session, redirect
from flask_mysqldb import MySQL
from IoTAssignment2 import app
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from IoTAssignment2 import pushBullet as pushBullet
#from cal_setup import get_calendar_service
import MySQLdb.cursors
import re
import sys
import hashlib
import pickle
import os.path
#import bluetooth
import json

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
        # generates a Salt and Hashes the Password with sha256
        salt = "lcyysk2NAQOJCHxkM1fA"
        saltPass = password+salt
        hashPass = hashlib.sha256(saltPass.encode())
        encryptPass = hashPass.hexdigest()
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, encryptPass,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, can access this in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['typeOfUser'] = account['typeOfUser']
            session['firstName'] = account['firstName']
            session['typeOfUser'] = account['typeOfUser']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
        
    return render_template('index.html', msg=msg)

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
        accessToken = ''
        MAC = ''
        # Generates a Salt and Hashes the Password with sha256
        salt = "lcyysk2NAQOJCHxkM1fA"
        saltPass = password+salt
        hashPass = hashlib.sha256(saltPass.encode())
        encryptPass = hashPass.hexdigest()
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks, got re from online sources
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
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (username, encryptPass, firstName, lastName, email, customer,accessToken, MAC))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

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
        #if session['typeOfUser'] == 'Customer':
            if request.method == 'GET':
                userid = session['id']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM bookings WHERE userid = %s', (userid,))
                history = cursor.fetchall()
                mysql.connection.commit()
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM bookings')
                allHistory = cursor.fetchall()
                mysql.connection.commit()


                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM cars WHERE broken = "ISSUE"')
                broken = cursor.fetchall()
                mysql.connection.commit()


                my_string = ""
                cout = 0 
                for row in broken:
                    my_string = my_string + row['longlat'] + '|'

                print(my_string)

                return render_template('home.html', allHistory=allHistory, typeOfUser=session['typeOfUser'], history=history, username=session['username'], broken=broken, my_string=my_string)
            else:
                return render_template('cars.html')
            
            return render_template('home.html', typeOfUser=session['typeOfUser'], username=session['username'])
        #else:
            #return render_template('adminHome.html', username=session['username'])
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
        return render_template('profile.html', typeOfUser=session['typeOfUser'], user=user)
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
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cars')
        cars = cursor.fetchall()

        my_string = ""
        cout = 0 
        for row in cars:
            my_string = my_string + row['longlat'] + '|'

        print(my_string)
        # Show the profile page with account info
        return render_template('cars.html', cars=cars, typeOfUser=session['typeOfUser'], my_string=my_string)
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

    

@app.route('/carManagement')
def carManagement():
    """
    An admin function that will let admin's perform database operations
    that regular users should not be able to.
    Legacy route
    """
    if 'loggedin' in session:
        # User is loggedin show them the home page
        if session['typeOfUser'] == 'Customer':
            return redirect(url_for('login'))
        else:
            return render_template('carManagement.html', typeOfUser=session['typeOfUser'])
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

            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars')
            carData = cursor.fetchall()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE id = %s', (idcar,))
            carIdData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE make = %s', (make,))
            carMakeData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE bodyType = %s', (bodyType,))
            carBodyTypeData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE colour = %s', (colour,))
            carColourData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE seats = %s', (seats,))
            carSeatsData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE location = %s', (location,))
            carLocationData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE cost = %s', (cost,))
            carCostData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE bookedBy = %s', (bookedBy,))
            carBookedByData = cursor.fetchone()
            mysql.connection.commit()
            
            

            print(type(carData))
            
            
            sqlExpression = 'SELECT * FROM cars'
            count = 0
            
            if idcar == '' and make == '' and bodyType == '' and colour == '' and seats == '' and location == '' and cost == '' and bookedBy == '':
                return redirect(url_for('cars'))
            else:
                sqlExpression = 'SELECT * FROM cars WHERE '
                if idcar != '':
                    if carIdData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' id = ' + idcar 
                        else:
                            sqlExpression = sqlExpression + ' id = ' + idcar
                            count = 1
                            print(count)
                            app.logger.info(count)
                    else:
                        return redirect(url_for('cars'))
                if make != '':
                    if carMakeData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' make = ' + '"' + make + '"'
                        else:
                            sqlExpression = sqlExpression + ' make = ' + '"' + make + '"'
                            count += 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('cars'))
                    
                if bodyType != '':
                    if carBodyTypeData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' bodyType = ' + '"' + bodyType + '"'
                        else:
                            sqlExpression = sqlExpression + ' bodyType = ' + '"' + bodyType + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                       return redirect(url_for('cars'))
                        
                if colour != '':
                    if carColourData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' colour = ' + '"' + colour + '"'
                        else:
                            sqlExpression = sqlExpression + ' colour = ' + '"' + colour + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('cars'))
                        
                if seats != '':
                    if carSeatsData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' seats = ' + '"' + seats + '"'
                        else:
                            sqlExpression = sqlExpression + ' seats = ' + '"' + seats + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('cars'))
                        
                if location != '':
                    if carLocationData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' location = ' + '"' + location + '"'
                        else:
                            sqlExpression = sqlExpression + ' location = ' + '"' + location + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('cars'))
                        
                if cost != '':
                   if carCostData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' cost = ' + '"' + cost + '"'
                        else:
                            sqlExpression = sqlExpression + ' cost = ' + '"' + cost + '"'
                            count = 1
                            app.logger.info(count)
                   else:
                        return redirect(url_for('cars'))
                        
                if bookedBy != '':
                    if carBookedByData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' bookedBy = ' + '"' + bookedBy + '"'
                        else:
                            sqlExpression = sqlExpression + ' bookedBy = ' + '"' + bookedBy + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('cars'))
                print (carMakeData)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*!!!!!!!!!!!!!!!!!!!!") 
                app.logger.info(sqlExpression)
                
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(sqlExpression)

                #cursor.execute('SELECT * FROM cars WHERE  bodyType = "Sedan"')

                #return redirect(url_for('cars'))
                cars = cursor.fetchall()
                # Show the profile page with account info
                my_string = ""
                cout = 0 
                for row in cars:
                    my_string = my_string + row['longlat'] + '|'

                print(my_string)
                # Show the profile page with account info
                return render_template('cars.html', cars=cars, typeOfUser=session['typeOfUser'], my_string=my_string)
                            
            
        
    return redirect(url_for('login'))


@app.route('/carBooking', methods=['GET', 'POST'])
def carBooking():
    
    """
    User inputs car by id they want to book and number of days and the session variable
    is parsed as well as the form data and creates an sql update in the database to
    allocate that car to them and also creates a google calendar event for that user.
    """
    if 'loggedin' in session:
        if request.method == 'POST':
            userid = session['id']
            username = session['username']
            firstName = session['firstName']
            date = datetime.now()
            
            bookingCarId = request.form['bookingCarId']
            bookingCarDays = request.form['bookingCarDays']


            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE id = %s', (bookingCarId,))               
            cars = cursor.fetchone()
            mysql.connection.commit()
            

            if cars != None:
                print("fhjsdfjhkdsfhsdjkfh------------------------------------------------------------")
                print(cars)
                if bookingCarDays.isdigit() == True:
                    print('-------------------------------------------------')
                    

                    
                    service = get_calendar_service()
                    
                    
                    d = datetime.now().date()
                    #change this for the amount of 
                    numDayBook = 1
                    startBook = datetime(d.year, d.month, d.day, 10)
                    endBook = datetime(d.year, d.month, d.day, 10)+timedelta(days=int(bookingCarDays))
                    start = startBook.isoformat()
                    end = endBook.isoformat()

                    event_result = service.events().insert(calendarId='primary',
                        body={ 
                            "summary": firstName, 
                            "description": cars['make'],
                            "start": {"dateTime": start, "timeZone": 'Australia/Sydney'}, 
                            "end": {"dateTime": end, "timeZone": 'Australia/Sydney'},
                        }
                    ).execute()

                    eventId = event_result['id']
                    
                    print("created event")
                    print("id: ", event_result['id'])
                    print("summary: ", event_result['summary'])
                    print("starts at: ", event_result['start']['dateTime'])
                    print("ends at: ", event_result['end']['dateTime'])


                    current = "current"
                    
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE cars SET bookedBy = %s WHERE id = %s', (username, bookingCarId,))
                    #cursor.execute('INSERT INTO `bookings`  

                    cursor.execute('INSERT INTO `bookings` (`calendarId`, `userid`, `firstName`, `date`, `daysBooked`, `carId`, `current`) VALUES (%s, %s, %s, %s, %s, %s, %s)', (eventId, userid, firstName, date, bookingCarDays, bookingCarId, current,))
                    mysql.connection.commit()
                    
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM cars')
                    #cursor.execute('SELECT * FROM cars WHERE bookedBy = %s', (available,))
                    #cursor.execute('SELECT * FROM cars WHERE make = "Ford Falcon"')
                    cars = cursor.fetchall()

                    my_string = ""
                    cout = 0 
                    for row in cars:
                        my_string = my_string + row['longlat'] + '|'

                    print(my_string)
                    # Show the profile page with account info
                    return render_template('cars.html', cars=cars, typeOfUser=session['typeOfUser'], my_string=my_string)

                else:
                    print(cars)
                    return redirect(url_for('cars'))
            else:
                      
                print('fdfhjdjhdfjhdfk')
                return redirect(url_for('cars'))
        else:
            return render_template('profile.html', typeOfUser=session['typeOfUser'])
        
    else:
        return redirect(url_for('login'))


@app.route('/cancelBooking', methods=['GET', 'POST'])
def cancelBooking():
    
    """
    User inputs the booking id that they want to cancel which is then updated in the
    google sql database and also the google calender event gets cancelled
    """
    
    if 'loggedin' in session:
        if request.method == 'POST':
            userid = session['id']
            
            emptyUsername = ""
            firstName = session['firstName']
            username = session['username']

            cancelBookingId = request.form['cancelCarId']

            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM bookings WHERE bookingId = %s', (cancelBookingId,))
            cancelBooking = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT bookingId FROM bookings')
            allBooking = cursor.fetchall()
            mysql.connection.commit()
            print("this fhithdjfh jskdfg hjkdsh fjksd fdjhskf sdjk :%s", allBooking)
            green = allBooking
            #intCancelBookingId = int(cancelBookingId)
            print(cancelBooking)
            print(green)
            print("here 1\/\/\/\/\/\/\/\/\/\/\/\/\/")

            if cancelBooking != None:
                
                    print("here 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
                    
                    cancelCarId = cancelBooking['carId']
                       
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM cars WHERE id = %s', (cancelCarId,))
                    cars = cursor.fetchone()
                    mysql.connection.commit()
                    
                    cancelled = "cancelled"
                       
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE cars SET bookedBy = %s WHERE id = %s', (emptyUsername, cancelCarId,))
                    cursor.execute('UPDATE bookings SET current = %s WHERE bookingId = %s', (cancelled, cancelBookingId,))
                    mysql.connection.commit()
                
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM bookings WHERE bookingId = %s', (cancelBookingId,))
                    booking = cursor.fetchone()
                    mysql.connection.commit()
                
                    #app.logger.info(cars['calendarId'])
                    print(booking['calendarId'])
                    service = get_calendar_service()
                    try:
                       service.events().delete(
                            calendarId='primary',
                            eventId=booking['calendarId'],
                        ).execute()
                    except:
                       print("Failed to delete event")
                    
                    print("Event deleted")


                    userid = session['id']
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM bookings WHERE userid = %s', (userid,))
                    history = cursor.fetchall()
                    mysql.connection.commit()
                    
                    return render_template('home.html', typeOfUser=session['typeOfUser'], username=username, history=history)

               
                
            else:
                userid = session['id']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM bookings WHERE userid = %s', (userid,))
                history = cursor.fetchall()
                mysql.connection.commit()

                return render_template('home.html', typeOfUser=session['typeOfUser'], username=username, history=history)
        else:
            return render_template('profile.html')
        
    else:
        return redirect(url_for('login'))
      
@app.route('/userhistory', methods=['POST'])
def userhistory():
    
    """
    Method to display history of bookings
    """
    if 'loggedin' in session:
        if request.method == 'POST':
            id = session['id']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM bookings WHERE userid = %d', (id,))
            history = cursor.fetchall()
            
            return render_template('userhistory.html', typeOfUser=session['typeOfUser'], history=history)
        else:
            return render_template('cars.html')
    else:
        return redirect(url_for('login'))
    
    
@app.route('/searchDatabase', methods=['GET', 'POST'])
def searchDatabase():
    """
    Displays users and cars tables for admin to query
    """
    # Check if user is loggedin
    if session['typeOfUser'] == 'Admin':
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cars')
        cars = cursor.fetchall()
        mysql.connection.commit()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        mysql.connection.commit()

        my_string = ""
        cout = 0 
        for row in cars:
            my_string = my_string + row['longlat'] + '|'

        print(my_string)
        # Show the profile page with account info
        return render_template('searchDatabase.html', users=users, cars=cars, typeOfUser=session['typeOfUser'], my_string=my_string)
    
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/adminCarQuery', methods=['POST'])
def adminCarQuery():
    """
    This function takes the data from a form and builds an sql query based
    on what variation of car attributes admin was looking for.
    Querying users and cars table for admins
    """
    #return render_template('searchDatabase.html')
    if session['typeOfUser'] == 'Admin':
        
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

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars')
            carData = cursor.fetchall()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE id = %s', (idcar,))
            carIdData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE make = %s', (make,))
            carMakeData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE bodyType = %s', (bodyType,))
            carBodyTypeData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE colour = %s', (colour,))
            carColourData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE seats = %s', (seats,))
            carSeatsData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE location = %s', (location,))
            carLocationData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE cost = %s', (cost,))
            carCostData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE bookedBy = %s', (bookedBy,))
            carBookedByData = cursor.fetchone()
            mysql.connection.commit()
            
            

            print(type(carData))
            
            
            sqlExpression = 'SELECT * FROM cars'
            count = 0
            
            if idcar == '' and make == '' and bodyType == '' and colour == '' and seats == '' and location == '' and cost == '' and bookedBy == '':
                return redirect(url_for('searchDatabase'))
            else:
                sqlExpression = 'SELECT * FROM cars WHERE '
                if idcar != '':
                    if carIdData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' id = ' + idcar 
                        else:
                            sqlExpression = sqlExpression + ' id = ' + idcar
                            count = 1
                            print(count)
                            app.logger.info(count)
                    else:
                        return redirect(url_for('searchDatabase'))
                if make != '':
                    if carMakeData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' make = ' + '"' + make + '"'
                        else:
                            sqlExpression = sqlExpression + ' make = ' + '"' + make + '"'
                            count += 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('searchDatabase'))
                    
                if bodyType != '':
                    if carBodyTypeData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' bodyType = ' + '"' + bodyType + '"'
                        else:
                            sqlExpression = sqlExpression + ' bodyType = ' + '"' + bodyType + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                       return redirect(url_for('searchDatabase'))
                        
                if colour != '':
                    if carColourData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' colour = ' + '"' + colour + '"'
                        else:
                            sqlExpression = sqlExpression + ' colour = ' + '"' + colour + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('searchDatabase'))
                        
                if seats != '':
                    if carSeatsData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' seats = ' + '"' + seats + '"'
                        else:
                            sqlExpression = sqlExpression + ' seats = ' + '"' + seats + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('searchDatabase'))
                        
                if location != '':
                    if carLocationData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' location = ' + '"' + location + '"'
                        else:
                            sqlExpression = sqlExpression + ' location = ' + '"' + location + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('searchDatabase'))
                        
                if cost != '':
                   if carCostData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' cost = ' + '"' + cost + '"'
                        else:
                            sqlExpression = sqlExpression + ' cost = ' + '"' + cost + '"'
                            count = 1
                            app.logger.info(count)
                   else:
                        return redirect(url_for('searchDatabase'))
                        
                if bookedBy != '':
                    if carBookedByData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' bookedBy = ' + '"' + bookedBy + '"'
                        else:
                            sqlExpression = sqlExpression + ' bookedBy = ' + '"' + bookedBy + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('searchDatabase'))
                print (carMakeData)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*!!!!!!!!!!!!!!!!!!!!") 
                app.logger.info(sqlExpression)
                
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(sqlExpression)

                #cursor.execute('SELECT * FROM cars WHERE  bodyType = "Sedan"')

                #return redirect(url_for('cars'))
                cars = cursor.fetchall()
                # Show the profile page with account info
                my_string = ""
                cout = 0 
                for row in cars:
                    my_string = my_string + row['longlat'] + '|'

                print(my_string)
                
                
                # Show the profile page with account info
                return render_template('searchDatabase.html', cars=cars, typeOfUser=session['typeOfUser'], my_string=my_string, users=users)
                            
            
        
    return redirect(url_for('login'))


@app.route('/adminUserQuery', methods=['POST'])
def adminUserQuery():
    """
    This function takes the data from a form and builds an sql query based
    on what variation of user attributes admin was looking for.
    If the form is blank it returns all the users available like the users route.
    """
    #return render_template('searchDatabase.html')
    if session['typeOfUser'] == 'Admin':
        
        if request.method == 'GET':
            
            idCar = request.form['id']
            cursor.execute('SELECT * FROM users')
            #cars = cursor.fetchone()
            #print(cars)
            #return render_template('cars.html', cars=cars)
            return render_template('home.html')
        else:

            idUser = request.form['idUser']
            username = request.form['username']
            password = request.form['password']
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            email = request.form['email']
            typeOfUser = request.form['typeOfUser']

            returned = 0

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars')
            cars = cursor.fetchall()
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users')
            userData = cursor.fetchall()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE id = %s', (idUser,))
            idUserData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            usernameData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE password = %s', (password,))
            passwordData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE firstName = %s', (firstName,))
            firstNameData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE lastName = %s', (lastName,))
            lastNameData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            emailData = cursor.fetchone()
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE typeOfUser = %s', (typeOfUser,))
            typeOfUserData = cursor.fetchone()
            mysql.connection.commit()

            

            print(type(userData))
            
            
            sqlExpression = 'SELECT * FROM users'
            count = 0
            
            if idUser == '' and username == '' and password == '' and firstName == '' and lastName == '' and email == '' and typeOfUser == '':
                return redirect(url_for('searchDatabase'))
            else:
                sqlExpression = 'SELECT * FROM users WHERE '
                if idUser != '':
                    if idUserData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' id = ' + idUser 
                        else:
                            sqlExpression = sqlExpression + ' id = ' + idUser
                            count = 1
                            print(count)
                            app.logger.info(count)
                    else:
                        return redirect(url_for('searchDatabase'))
                if username != '':
                    if usernameData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' username = ' + '"' + username + '"'
                        else:
                            sqlExpression = sqlExpression + ' username = ' + '"' + username + '"'
                            count += 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('searchDatabase'))
                    
                if password != '':
                    if passwordData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' password = ' + '"' + password + '"'
                        else:
                            sqlExpression = sqlExpression + ' password = ' + '"' + password + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                       return redirect(url_for('searchDatabase'))
                        
                if firstName != '':
                    if firstNameData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' firstName = ' + '"' + firstName + '"'
                        else:
                            sqlExpression = sqlExpression + ' firstName = ' + '"' + firstName + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('searchDatabase'))
                        
                if lastName != '':
                    if lastNameData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' lastName = ' + '"' + lastName + '"'
                        else:
                            sqlExpression = sqlExpression + ' lastName = ' + '"' + lastName + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('searchDatabase'))
                        
                if email != '':
                    if emailData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' email = ' + '"' + email + '"'
                        else:
                            sqlExpression = sqlExpression + ' email = ' + '"' + email + '"'
                            count = 1
                            app.logger.info(count)
                    else:
                        return redirect(url_for('searchDatabase'))
                        
                if typeOfUser != '':
                   if typeOfUserData != None:
                        if count != 0:
                            sqlExpression = sqlExpression + ' AND ' + ' typeOfUser = ' + '"' + typeOfUser + '"'
                        else:
                            sqlExpression = sqlExpression + ' typeOfUser = ' + '"' + typeOfUser + '"'
                            count = 1
                            app.logger.info(count)
                   else:
                        return redirect(url_for('searchDatabase'))

                #print (carMakeData)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*!!!!!!!!!!!!!!!!!!!!") 
                app.logger.info(sqlExpression)
                
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(sqlExpression)

                #cursor.execute('SELECT * FROM cars WHERE  bodyType = "Sedan"')

                #return redirect(url_for('cars'))
                users = cursor.fetchall()
                # Show the profile page with account info
                #my_string = ""
                #cout = 0 
                #for row in cars:
                #    my_string = my_string + row['longlat'] + '|'

                #print(my_string)
                # Show the profile page with account info
                return render_template('searchDatabase.html', users=users, typeOfUser=session['typeOfUser'], cars=cars)
                            
            
        
    return redirect(url_for('login'))


@app.route('/reportCar', methods=['GET', 'POST'])
def reportCar():
    
    """
    Admin uses this route to issue a notification for an engineer to fix the car by
    updating the broken column on a car by filling out a form and sending the data
    to the google database.
    """
    
    if session['typeOfUser'] == 'Admin':
        if request.method == 'POST':

            idReport = request.form['idReport']
            broken = 'ISSUE'

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE cars SET broken = %s WHERE id = %s', (broken, idReport,))
            pushBullet.pushBullet()  
            mysql.connection.commit()
            return redirect(url_for('searchDatabase'))
        else:
            return render_template('profile.html')
        
    else:
        return redirect(url_for('login')) 

@app.route('/editCar')
def editCar():
    
    """
    default edit car page for the admin
    """
    
    if session['typeOfUser'] == 'Admin':
        return render_template('editCar.html')
    else:
        return redirect(url_for('login'))
                 
@app.route('/addCar', methods=['GET', 'POST'])
def addCar():
    
    """
    Admin add car method to fill out a form that is then
    inputted into the google database for further hire by users
    """
    
    if session['typeOfUser'] == 'Admin':
        if request.method == 'POST':

            addmake = request.form['addmake']
            addbodyType = request.form['addbodyType']
            addcolour = request.form['addcolour']
            addseats = request.form['addseats']
            addlocation = request.form['addlocation']
            addcost = request.form['addcost']
            addbookedby = ''
            addlonglat = ''
            addreturned = ''
            addbroken = ''

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO cars VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (addmake, addbodyType, addcolour, addseats, addlocation, addcost, addbookedby, addlonglat, addreturned, addbroken))
            #cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (username, encryptPass, firstName, lastName, email, customer,accessToken, MAC))
            
            mysql.connection.commit()
            return render_template('editCar.html')
        else:
            return render_template('profile.html')
        
    else:
        return redirect(url_for('login')) 


@app.route('/updateCar', methods=['GET', 'POST'])
def updateCar():
    
    """
    Admin updates car values by way of form, specifies car id and uses that
    to identify which car is being updated. Values left blank will not be updated
    """
    
    if session['typeOfUser'] == 'Admin':
        if request.method == 'POST':

            selectcarId = request.form['selectcarId']
            updatemake = request.form['updatemake']
            updatebodyType = request.form['updatebodyType']
            updatecolour = request.form['updatecolour']
            updateseats = request.form['updateseats']
            updatelocation = request.form['updatelocation']
            updatecost = request.form['updatecost']
            updatebookedBy = ''
            updatelonglat = ''
            updatereturned = ''
            updatebroken = ''

            if selectcarId != '':
                if updatemake != '':
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE cars SET make = %s WHERE id = %s', (updatemake, selectcarId,))  
                    mysql.connection.commit()

                if updatebodyType != '':
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE cars SET bodyType = %s WHERE id = %s', (updatebodyType, selectcarId,))  
                    mysql.connection.commit()

                if updatecolour != '':
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE cars SET colour = %s WHERE id = %s', (updatecolour, selectcarId,))  
                    mysql.connection.commit()

                if updateseats != '':
                    if updateseats.isdigit() == True:
                        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        cursor.execute('UPDATE cars SET seats = %s WHERE id = %s', (updateseats, selectcarId,))  
                        mysql.connection.commit()
                    else:
                        print("note a number!!!! uwu")

                if updatelocation != '':
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE cars SET location = %s WHERE id = %s', (updatelocation, selectcarId,))  
                    mysql.connection.commit()

                if updatecost != '':
                    if updatecost.isdigit() == True:
                        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        cursor.execute('UPDATE cars SET cost = %s WHERE id = %s', (updatecost, selectcarId,))  
                        mysql.connection.commit()
                    else:
                        print("note a number!!!! uwu")

                return render_template('editCar.html')


        else:
            return render_template('profile.html')
        
    else:
        return redirect(url_for('login')) 


@app.route('/deleteCar', methods=['GET', 'POST'])
def deleteCar():

    """
    Admin specifies car id to delete which is removed from the databse.
    """
    
    if session['typeOfUser'] == 'Admin':
        if request.method == 'POST':


            deleteCarId = request.form['deleteid']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM cars WHERE id = %s', (deleteCarId,))
            deleteCarData = cursor.fetchone()
            mysql.connection.commit()

            if deleteCarData != None:
                
                    deleteCar = deleteCarData['id']
                       
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('DELETE FROM cars WHERE id = %s', (deleteCar,))
                    mysql.connection.commit()
                              
                    return render_template('editCar.html')
                
            else:
                return render_template('editCar.html')
        else:
            return render_template('profile.html')
        
    else:
        return redirect(url_for('login'))    


@app.route('/editUser')
def editUser():
    
    """
    default edit user page for the admin
    """
    
    if session['typeOfUser'] == 'Admin':
        return render_template('editUser.html')
    else:
        return redirect(url_for('login'))
                 
@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    
    """
    Admin add user method to fill out a form that is then
    inputted into the google database for further use
    """
    
    if session['typeOfUser'] == 'Admin':
        if request.method == 'POST':

            addusername = request.form['addusername']
            addpassword = request.form['addpassword']
            addfirstName = request.form['addfirstName']
            addlastName = request.form['addlastName']
            addemail = request.form['addemail']
            addtypeofuser = request.form['addtypeofuser']
            addaccesstoken = ''
            mac = ''
            # generates a Salt and Hashes the Password with sha256
            salt = "lcyysk2NAQOJCHxkM1fA"
            saltPass = addpassword+salt
            hashPass = hashlib.sha256(saltPass.encode())
            encryptPass = hashPass.hexdigest()


            if not re.match(r'[^@]+@[^@]+\.[^@]+', addemail):
                msg = 'Invalid email address!'
                print("bad--------------------------------------------------------------------")
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (addusername, encryptPass, addfirstName, addlastName, addemail, addtypeofuser, addaccesstoken, mac))
                #cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (username, encryptPass, firstName, lastName, email, customer,accessToken, MAC))
                
            mysql.connection.commit()
            return render_template('editUser.html')
        else:
            return render_template('profile.html')
        
    else:
        return redirect(url_for('login')) 


@app.route('/updateUser', methods=['GET', 'POST'])
def updateUser():

    """
    Admin updates user values by way of form, specifies car id and uses that
    to identify which user is being updated. Values left blank will not be updated
    """
    
    if session['typeOfUser'] == 'Admin':
        if request.method == 'POST':

            #idReport = request.form['idReport']
            #broken = 'ISSUE'

            #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #cursor.execute('UPDATE cars SET broken = %s WHERE id = %s', (broken, idReport,))  
            #mysql.connection.commit()
            #return redirect(url_for('searchDatabase'))
            selectId = request.form['selectId']
            editusername = request.form['updateusername']
            editpassword = request.form['updatepassword']
            editfirstName = request.form['updatefirstName']
            editlastName = request.form['updatelastName']
            editemail = request.form['updateemail']
            edittypeofuser = request.form['updatetypeofuser']
            editaccesstoken = ''
            mac = ''
            # generates a Salt and Hashes the Password with sha256
            salt = "lcyysk2NAQOJCHxkM1fA"
            saltPass = editpassword+salt
            hashPass = hashlib.sha256(saltPass.encode())
            encryptPass = hashPass.hexdigest()


            #This is probably wrong uwu uwu uwu uwu uwu uwu uwu uwu uwu uwu uwu uwu uwu uwu uwu uwu
            if selectId != '':
                if editusername != '':
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE users SET username = %s WHERE id = %s', (editusername, selectId,))  
                    mysql.connection.commit()
                    
                if editpassword != '':
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE users SET password = %s WHERE id = %s', (encryptPass, selectId,))  
                    mysql.connection.commit()

                if editfirstName != '':
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE users SET firstName = %s WHERE id = %s', (editfirstName, selectId,))  
                    mysql.connection.commit()

                if editlastName != '':
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE users SET lastName = %s WHERE id = %s', (editlastName, selectId,))  
                    mysql.connection.commit()

                if editemail != '':
                    if not re.match(r'[^@]+@[^@]+\.[^@]+', editemail):
                        msg = 'Invalid email address!'
                        print("bad__________________________---------------------- uwu")
                    else:
                        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        cursor.execute('UPDATE users SET email = %s WHERE id = %s', (editemail, selectId,))  
                        mysql.connection.commit()

                if edittypeofuser != '':
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    #don't know what this is called 
                    cursor.execute('UPDATE users SET typeOfUser = %s WHERE id = %s', (edittypeofuser, selectId,))  
                    mysql.connection.commit()

                return render_template('editUser.html')
                
            
        else:
            return render_template('profile.html')
        
    else:
        return redirect(url_for('login')) 
            


@app.route('/deleteUser', methods=['GET', 'POST'])
def deleteUser():

    """
    Admin specifies user id to delete which is removed from the databse.
    """
    
    if session['typeOfUser'] == 'Admin':
        if request.method == 'POST':


            deleteUserId = request.form['deleteUid']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE id = %s', (deleteUserId,))
            deleteUserData = cursor.fetchone()
            mysql.connection.commit()

            if deleteUserData != None:
                
                    deleteUser = deleteUserData['id']
                       
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('DELETE FROM users WHERE id = %s', (deleteUser,))
                    mysql.connection.commit()
                              
                    return render_template('editUser.html')
                
            else:
                return render_template('editUser.html')
        else:
            return render_template('profile.html')
        
    else:
        return redirect(url_for('login'))    

@app.route('/searchBooking', methods=['GET','POST'])
def searchBooking():
    """
    This route lets an admin search through the booking history for a specific
    cars bookings.
    """
    # Check if user is loggedin
    if session['typeOfUser'] == 'Admin':
        if request.method == 'POST':
        
       
            searchID=request.form['searchCarId']
            if searchID != '':
                if searchID.isdigit() == True:
                    
                    # We need all the account info for the user so we can display it on the profile page
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM bookings WHERE carId = %s', (searchID,))
                    allHistory = cursor.fetchall()

                    # Show the profile page with account info
                    return render_template('home.html', allHistory=allHistory, typeOfUser=session['typeOfUser'], username=session['username'])
        
                else:
                    return redirect(url_for('home'))
            else:
                return redirect(url_for('home'))
            
            
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'credentials.json'

def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

