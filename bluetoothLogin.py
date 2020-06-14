#References
#RMIT Programming Internet of Things Tutorial code achive

import bluetooth
import time
import MySQLdb.cursors


MYSQL_HOST = "35.244.72.137"
MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"
MYSQL_DB = "Peopl"

    
connection = None
if(connection == None):
    connection = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)


def search():
    """
    Function searches for nearby phones using bluetooth, if known MAC is found,
    car is unlocked. Database is updated. 
    """
    while True:
        print("Set AP Car ID")
        carID = input("Enter Car ID: ")
        
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        
        nearby = bluetooth.discover_devices()
        

        for mac_address in nearby:
            
            while bluetooth.lookup_name(mac_address, timeout=5):
                mac = mac_address
            
                
                cursor.execute('SELECT * FROM users WHERE MAC= %s', (mac,))
                account = cursor.fetchone()
                
                #if engineer.matchMac(mac) == True:
                if account:
                    print("Found Engineer")
                    
                    print("Unlocking Vehicle")
                    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
                    carStr = "Repairing"
                    
                    cursor.execute('UPDATE cars SET returned=%s WHERE id=%s', (carStr, carID))
                    connection.commit()
                    
                    print(mac_address)
                    
                    return True
                else:
                    print("No Engineer Nearby")
                    return False
            
            
        else:
            print("Could not find target device nearby...")
            return False
            

