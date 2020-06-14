#References
#RMIT Programming Internet of Things Tutorial code achive

import MySQLdb.cursors
import hashlib


class engineer():
    """
    Function connects to database,
    
    """
    
    #Database connection
    MYSQL_HOST = "35.244.72.137"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "1234"
    MYSQL_DB = "Peopl"

    
    connection = None
    if(connection == None):
        connection = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)
 
    
    
    def updater():
        """
        Function used to update users mac and token values
        """
        while True: 
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            user = "9"
            #token = "o.DKJYYAlco6vYNs09Crn7jdR1bRtyAo5k"
            #token = "hellohel"
            #mac = "pur"
            #cursor.execute('UPDATE users SET accessToken=%s WHERE id=%s', (token, user))
            connection.commit()
            mac = "14:9F:3C:76:B6:04"
            cursor.execute('UPDATE users SET MAC=%s WHERE id=%s', (mac, user))
            
            connection.commit()
            
            cursor.execute('SELECT * FROM users')
            print(cursor.fetchall())
            break
    
    def updateCars():
        """
        Function used to update car state to Working
        """
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        carID = "3"
        state = "Working"
        cursor.execute('UPDATE cars SET broken=%s WHERE id=%s', (state, carID))
        connection.commit()
    
    def unlockCars():
        """
        Function used to update car state to Repairing
        """
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        carStr = "Repairing"
        carID = "3"
        cursor.execute('UPDATE cars SET returned=%s WHERE id=%s', (carStr, carID))
        connection.commit()
        
        
    def matchMac(mac):
        """
        Function used to match given mac to database to find matches
        """
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                            
        cursor.execute('SELECT * FROM users WHERE MAC= %s', (mac, ))
                    
        account = cursor.fetchone()
            
        if account:
            return True
        else:
            print("No matching MAC Address")
            return False
            
    
    
engineer()

