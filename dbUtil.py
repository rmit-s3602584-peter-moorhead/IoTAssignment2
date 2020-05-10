import MySQLdb

class DatabaseUtils:
    HOST = "35.244.72.137"
    USER = "root"
    PASSWORD = "1234"
    DATABASE = "Peopl"

    def __init__(self, connection = None):
        if(connection == None):
            connection = MySQLdb.connect(DatabaseUtils.HOST, DatabaseUtils.USER,
                DatabaseUtils.PASSWORD, DatabaseUtils.DATABASE)
        self.connection = connection

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def createPersonTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `users` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `username` varchar(50) NOT NULL,
                `password` varchar(255) NOT NULL,
                `firstName` varchar(15) NOT NULL,
                `lastName` varchar(50) NOT NULL,
                `email` varchar(100) NOT NULL,
                `typeOfUser` varchar(10) NOT NULL,
                PRIMARY KEY (`id`)
                )""")
        self.connection.commit()
    
#    def createPersonTable(self):
#        with self.connection.cursor() as cursor:
#            cursor.execute("""
#                CREATE TABLE IF NOT EXISTS `cars` (
#                `id` int(11) NOT NULL AUTO_INCREMENT,
#                `make` varchar(50) NOT NULL,
#                `bodyType` varchar(10) NOT NULL,
#                `colour` varchar(15) NOT NULL,
#                `seats` int(2) NOT NULL,
#                `location` varchar(20) NOT NULL,
#                `cost` int(4) NOT NULL,
#                `bookedBy` varchar(20) NOT NULL,
#                PRIMARY KEY (`id`)
#                )""")
#        self.connection.commit()
    
    def dropTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("DROP TABLE Users")
        self.connection.commit()
    
    def insertPerson(self, name):
        with self.connection.cursor() as cursor:
            #cursor.execute("INSERT INTO `cars` (`id`, `make`, `bodyType`, `colour`, `seats`, `location`, `cost`, `bookedBy`) VALUES (1, 'Ford Falcon', 'Sedan', 'Red', 4, 'Melbourne', 20, 'Peter')")
            cursor.execute("INSERT INTO `users` (`id`, `username`, `password`, `firstName`, `lastName`, `email`, `typeOfUser`) VALUES (1, 'admin', 'admin', 'admin', 'admin', 'admin@admin.com', 'Admin')")
            cursor.execute("INSERT INTO `users` (`id`, `username`, `password`, `firstName`, `lastName`, `email`, `typeOfUser`) VALUES (2, 'peter', 'peter', 'peter', 'moorhead', 'peter@test.com', 'Manager')")
            cursor.execute("INSERT INTO `users` (`id`, `username`, `password`, `firstName`, `lastName`, `email`, `typeOfUser`) VALUES (3, 'tim', 'tim', 'tim', 'dalzotto', 'tim@test.com', 'Engineer')")
            cursor.execute("INSERT INTO `users` (`id`, `username`, `password`, `firstName`, `lastName`, `email`, `typeOfUser`) VALUES (4, 'joel', 'joel', 'joel', 'tan', 'joel@test.com', 'Customer')")
            cursor.execute("INSERT INTO `users` (`id`, `username`, `password`, `firstName`, `lastName`, `email`, `typeOfUser`) VALUES (5, 'taylor', 'taylor', 'taylor', 'cairns', 'taylor@test.com', 'Customer')")
            
            cursor.execute("insert into Person (Name) values (%s)", (name,))
        self.connection.commit()

        return cursor.rowcount == 1
    
    def insertCar(self, carId, make, body, colour, seats, location, cost, bookedBy):
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO `cars` (`id`, `make`, `bodyType`, `colour`, `seats`, `location`, `cost`, `bookedBy`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (carId, make, body, colour, seats, location, cost, bookedBy,))
            #cursor.execute("insert into Person (Name) values (%s)", (name,))
        self.connection.commit()

        return cursor.rowcount == 1
    
    def deleteCar(self, carId):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from cars where id = %s", (carId,))
        self.connection.commit()

    def getPeople(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select id, username from users")
            return cursor.fetchall()
    
    def getCars(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select id, make from cars")
            return cursor.fetchall()

    def deletePerson(self, personID):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from Person where PersonID = %s", (personID,))
        self.connection.commit()