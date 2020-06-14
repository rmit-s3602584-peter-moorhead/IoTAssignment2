#References
#RMIT Programming Internet of Things Tutorial 10 code achive


import speech_recognition as sr
import MySQLdb, subprocess
import MySQLdb.cursors
import hashlib

MYSQL_HOST = "35.244.72.137"
MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"
MYSQL_DB = "Peopl"

MIC_NAME = "USB2.0 Camera: Audio (hw:1,0)"

connection = None
if(connection == None):
    connection = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)

def adminTts():
    """
    Function runs all modules involved with Admin searching Cars Via Voice Recognition
    """
    
    acc = verifyLogin()
    
    if acc == False:
        print("Invalid Credentials")
        return
    if acc == True:
        print("Credentials Verified - Welcome")
        
    carID = getCarID()

    if(carID is None):
        print("Failed to get Car ID.")
        return

    
    print("Looking for car with Identifcation Number '{}'...".format(carID))
    

    rows = searchCarID(carID)
    if(rows):
        print("Found:", rows)
    else:
        print("No results found.")

def getCarID():
    """
    Function uses microphone for voice recognition to find details of an item based on ID
    """
    #Find Microphone based on name
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        if(microphone_name == MIC_NAME):
            device_id = i
            break

    #Record Audio
    r = sr.Recognizer()
    with sr.Microphone(device_index = device_id) as source:
        # clear console of errors
        subprocess.run("clear")

        #Adjust for surrounding noise
        r.adjust_for_ambient_noise(source)

        print("Say Car Id To Search")
        try:
            audio = r.listen(source, timeout = 1.5)
        except sr.WaitTimeoutError:
            return None

    # recognize speech using Google Speech Recognition
    carID = None
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        carID = r.recognize_google(audio)
    except(sr.UnknownValueError, sr.RequestError):
        pass
    finally:
        return carID

def searchCarID(carID):
    """
    Function accepts input and finds car with specific ID
    """
    
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("select * from cars where id = %s", (carID,))
    
    rows = cursor.fetchall()

    connection.close()

    return rows

def verifyLogin():
    print("Welcome Admin")
    """
    Function accepts input and verifies user login with database.
    If user enters correct data, function returns true. 
    """
    print("Enter Login Credentials")
    us = input("Enter Username: ")
    pa = input("Enter Password: ")
    salt = "lcyysk2NAQOJCHxkM1fA"
    saltPass = pa+salt
    hashPass = hashlib.sha256(saltPass.encode())
    enPa = hashPass.hexdigest()
    utype = "Admin"
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)          
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s AND typeOfUser=%s', (us, enPa, utype, ))
    
                    
    account = cursor.fetchone()
            
    if account:
        return True
    else:
        return False

adminTts()

