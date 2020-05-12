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
                `userid` int(11) NOT NULL,
                `firstName` varchar(50) NOT NULL,
                `date` varchar(255) NOT NULL,
                `booked` BIT(1) NOT NULL,
                PRIMARY KEY (`userid`)
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
                `returned` BOOL NOT NULL,
                PRIMARY KEY (`id`)
                )""")
        self.connection.commit()
        
    def dropTable(self):
        with self.connection.cursor() as cursor:
            cursor.execute("DROP TABLE cars")
        self.connection.commit()
    
    def insertPerson(self, name):
        with self.connection.cursor() as cursor:
            #cursor.execute("INSERT INTO `cars` (`id`, `make`, `bodyType`, `colour`, `seats`, `location`, `cost`, `bookedBy`, `returned`) VALUES (1, 'Ford Falcon', 'Sedan', 'Red', 4, 'Melbourne', 20, 'Peter', 0)")
            cursor.execute("INSERT INTO `cars` VALUES (1,'Ford Falcon','Sedan','Red',4,'Melbourne',20,'', TRUE),(2,'Ford Falcon','Sedan','Red',4,'Melbourne',20,'', TRUE),(3,'Ford Fiesta','Hatch','Blue',2,'Sydney',40,'', TRUE),(4,'Lamborghini Aventador','4WD','Yellow',6,'Hobart',60,'', TRUE),(5,'Nissan Patrol','Ute','Red',3,'Melbourne',20,'', TRUE),(6,'A bus','Truck','Black',4,'Perth',50,'', TRUE),(7,'Mazda 3','Sedan','Green',5,'Brisbane',70,'', TRUE),(8,'Ford Falcon','Sedan','White',5,'Brisbane',10,'', TRUE),(9,'Honda Accord','Hatch','White',8,'Sydney',20,'', TRUE),(10,'Ford Territory','Sedan','Purple',4,'Melbourne',100,'', TRUE),(11,'Holden Ute','Sedan','Yellow',4,'Melbourne',20,'', TRUE),(12,'Subaru Imprezza','Hatch','Blue',4,'Ivanhoe',69,'Cathy', FALSE)")
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