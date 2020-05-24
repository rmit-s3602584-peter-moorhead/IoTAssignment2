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
    
    def createBookingsTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `bookings` (
                `bookingId` int(11) NOT NULL AUTO_INCREMENT,
                `calendarId` varchar(35) NOT NULL,
                `userid` int(11) NOT NULL,
                `firstName` varchar(50) NOT NULL,
                `date` varchar(255) NOT NULL,
                `daysBooked` int(10) NOT NULL,
                `carId` int(10) NOT NULL,
                `current` varchar(10),

                PRIMARY KEY (`bookingId`)

                )""")
        self.connection.commit()
    
    def createCarsTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `cars` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `make` varchar(50) NOT NULL,
                `bodyType` varchar(10) NOT NULL,
                `colour` varchar(15) NOT NULL,
                `seats` int(2) NOT NULL,
                `location` varchar(20) NOT NULL,
                `cost` int(4) NOT NULL,
                `bookedBy` varchar(20) NOT NULL,
                `longlat` varchar(25),
                `returned` varchar(20) NOT NULL,
                PRIMARY KEY (`id`)
                )""")
        self.connection.commit()
        
    def dropTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("DROP TABLE bookings")
        self.connection.commit()
    
    def insertPerson(self, name):
        with self.connection.cursor() as cursor:

            #cursor.execute('UPDATE cars SET bookedBy = "Test" WHERE id = 2')
                          #'UPDATE cars SET bookedBy = "admin" WHERE id = 2'
            #cursor.execute("INSERT INTO `cars` VALUES (1,'Ford Falcon','Sedan','Red',4,'Melbourne',20,'', TRUE),(2,'Ford Falcon','Sedan','Red',4,'Melbourne',20,'', TRUE),(3,'Ford Fiesta','Hatch','Blue',2,'Sydney',40,'', TRUE),(4,'Lamborghini Aventador','4WD','Yellow',6,'Hobart',60,'', TRUE),(5,'Nissan Patrol','Ute','Red',3,'Melbourne',20,'', TRUE),(6,'A bus','Truck','Black',4,'Perth',50,'', TRUE),(7,'Mazda 3','Sedan','Green',5,'Brisbane',70,'', TRUE),(8,'Ford Falcon','Sedan','White',5,'Brisbane',10,'', TRUE),(9,'Honda Accord','Hatch','White',8,'Sydney',20,'', TRUE),(10,'Ford Territory','Sedan','Purple',4,'Melbourne',100,'', TRUE),(11,'Holden Ute','Sedan','Yellow',4,'Melbourne',20,'', TRUE),(12,'Subaru Imprezza','Hatch','Blue',4,'Ivanhoe',69,'Cathy', FALSE)")

            #cursor.execute('UPDATE cars SET bookedBy = "" WHERE id = 2')
            #cursor.execute('UPDATE cars SET bookedBy = "" WHERE id = 3')
            #cursor.execute('UPDATE cars SET bookedBy = "" WHERE id = 4')
            #cursor.execute('UPDATE cars SET bookedBy = "" WHERE id = 5')
            #cursor.execute('UPDATE cars SET bookedBy = "" WHERE id = 6')
            #cursor.execute('UPDATE cars SET bookedBy = "" WHERE id = 7')
            #cursor.execute('UPDATE cars SET bookedBy = "" WHERE id = 8')
                          #'UPDATE cars SET bookedBy = "admin" WHERE id = 2'
            cursor.execute("INSERT INTO `cars` VALUES (1,'Ford Falcon','Sedan','Red',4,'Melbourne',20,'', '-37.881372,145.075725', 'Returned'),(2,'Ford Falcon','Sedan','Red',4,'Melbourne',20,'', '-37.871357,145.041828', 'Returned'),(3,'Ford Fiesta','Hatch','Blue',2,'Sydney',40,'', '-37.859541,145.036109', 'Returned'),(4,'Lamborghini Aventador','4WD','Yellow',6,'Hobart',60,'', '-37.773855,144.911660', 'Returned'),(5,'Nissan Patrol','Ute','Red',3,'Melbourne',20,'', '-37.773855,144.911660', 'Returned'),(6,'A bus','Truck','Black',4,'Perth',50,'', '-37.766718,144.909045', 'Returned'),(7,'Mazda 3','Sedan','Green',5,'Brisbane',70,'', '-37.785097,144.950881', 'Returned'),(8,'Ford Falcon','Sedan','White',5,'Brisbane',10,'', '-37.799069,144.961058', 'Returned'),(9,'Honda Accord','Hatch','White',8,'Sydney',20,'', '-37.805467,144.980526', 'Returned'),(10,'Ford Territory','Sedan','Purple',4,'Melbourne',100,'', '-37.830743,144.962914', 'Returned'),(11,'Holden Ute','Sedan','Yellow',4,'Melbourne',20,'', '', 'Returned'),(12,'Subaru Imprezza','Hatch','Blue',4,'Ivanhoe',69,'Cathy', '-37.817116,144.979985', 'In use')")

            
            
            #cursor.execute("INSERT INTO `users` (`id`, `username`, `password`, `firstName`, `lastName`, `email`, `typeOfUser`) VALUES (1, 'admin', 'admin', 'admin', 'admin', 'admin@admin.com', 'Admin')")
            #cursor.execute("INSERT INTO `users` (`id`, `username`, `password`, `firstName`, `lastName`, `email`, `typeOfUser`) VALUES (2, 'peter', 'peter', 'peter', 'moorhead', 'peter@test.com', 'Manager')")
            #cursor.execute("INSERT INTO `users` (`id`, `username`, `password`, `firstName`, `lastName`, `email`, `typeOfUser`) VALUES (3, 'tim', 'tim', 'tim', 'dalzotto', 'tim@test.com', 'Engineer')")
            #cursor.execute("INSERT INTO `users` (`id`, `username`, `password`, `firstName`, `lastName`, `email`, `typeOfUser`) VALUES (4, 'joel', 'joel', 'joel', 'tan', 'joel@test.com', 'Customer')")
            #cursor.execute("INSERT INTO `users` (`id`, `username`, `password`, `firstName`, `lastName`, `email`, `typeOfUser`) VALUES (5, 'taylor', 'taylor', 'taylor', 'cairns', 'taylor@test.com', 'Customer')")
            
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
            cursor.execute("select calendarId, bookingId from bookings")
            return cursor.fetchall()
    
    def getCars(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select bookingId from bookings")
            return cursor.fetchall()

    def deletePerson(self, personID):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from Person where PersonID = %s", (personID,))
        self.connection.commit()
