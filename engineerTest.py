# Reference: https://docs.python.org/2/library/unittest.html
import unittest
import hashlib
import MySQLdb.cursors


MYSQL_HOST = "35.244.72.137"
MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"
MYSQL_DB = "Peopl"

    
connection = None
if(connection == None):
    connection = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB)

class TestStringMethods(unittest.TestCase):
    """
    Function runs all Engineer Related Tests 
    """
    def test_login(self):
        """
        Function runs test to verify Admin login
        """
        print("Admin Verification Test")
        login = "admin1"
        self.assertEqual(testVerifyLogin(login, login), True)
        
    def test_cred(self):
        """
        Function runs test to verify Engineer Login
        """
        print("Login Verification Test")
        login = "Engineer1"
        self.assertEqual(testCred(login, login), True)
    def test_carID(self):
        """
        Function runs test to find Car By ID
        """
        print("Search Car By ID Test")
        carID = "1"
        self.assertEqual(testCarID(carID), True)
        
        




def testVerifyLogin(us, pa):
    
    """
    Test Function accepts input and verifies user login with database.
    Also checks type of User is Admin
    If user enters correct data, function returns true. 
    """
    
    us = us
    pa = pa
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

def testCred(us, pa):
    """
    Test Function accepts input and verifies user login with database.
    If user enters correct data, function returns true. 
    """
    
    us = us
    pa = pa
    
    salt = "lcyysk2NAQOJCHxkM1fA"
    saltPass = pa+salt
    hashPass = hashlib.sha256(saltPass.encode())
    enPa = hashPass.hexdigest()
    utype = "Engineer"
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)          
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s AND typeOfUser=%s', (us, enPa, utype, ))
    
                    
    account = cursor.fetchone()
            
    if account:
        return True
    else:
        return False



def testCarID(carID):
    """
    Test Function accepts input and finds car with specific ID
    """
    
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    if cursor.execute("select * from cars where id = %s", (carID,)):
        return True


    














if __name__ == "__main__":
    unittest.main()