import MySQLdb.cursors
import hashlib


def engineer():
    
    #Database connection
    MYSQL_HOST = "35.244.72.137"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "1234"
    MYSQL_DB = "Peopl"

    
    connection = None
    if(connection == None):
        connection = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
    
    def updater():
        while True: 
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            user = "3"
            #token = "o.DKJYYAlco6vYNs09Crn7jdR1bRtyAo5k"
            token = "hellohel"
            mac = "pur"
            cursor.execute('UPDATE users SET accessToken=%s WHERE id=%s', (token, user))
            connection.commit()
            #mac = "14:9F:3C:76:B6:04"
            cursor.execute('UPDATE users SET MAC=%s WHERE id=%s', (mac, user))
            
            connection.commit()
            
            cursor.execute('SELECT * FROM users')
            print(cursor.fetchall())
            break
    
    def updateCars():
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        carID = "3"
        state = "Working"
        cursor.execute('UPDATE cars SET broken=%s WHERE id=%s', (state, carID))
    
    def unlockCars():
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        carStr = "Repairing"
        carID = "3"
        cursor.execute('UPDATE cars SET returned=%s WHERE id=%s', (carStr, carID))
        
        
    def matchMac(mac):
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                            
        cursor.execute('SELECT * FROM users WHERE MAC= %s', (mac, ))
                    
        account = cursor.fetchone()
            
        if account:
            return True
        else:
            print("No matching MAC Address")
            
    
    
    
    

