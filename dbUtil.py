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
                CREATE TABLE IF NOT EXISTS `cars` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `make` varchar(50) NOT NULL,
                `bodyType` varchar(10) NOT NULL,
                `colour` varchar(15) NOT NULL,
                `seats` int(2) NOT NULL,
                `location` varchar(20) NOT NULL,
                `cost` int(4) NOT NULL,
                `bookedBy` varchar(20) NOT NULL,
                PRIMARY KEY (`id`)
                )""")
        self.connection.commit()

    def insertPerson(self, name):
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO `cars` (`id`, `make`, `bodyType`, `colour`, `seats`, `location`, `cost`, `bookedBy`) VALUES (1, 'Ford Falcon', 'Sedan', 'Red', 4, 'Melbourne', 20, 'Peter')")
            #cursor.execute("INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES (1, 'test', 'test', 'test@test.com')")
            cursor.execute("insert into Person (Name) values (%s)", (name,))
        self.connection.commit()

        return cursor.rowcount == 1

    def getPeople(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select PersonID, Name from Person")
            return cursor.fetchall()

    def deletePerson(self, personID):
        with self.connection.cursor() as cursor:
            # Note there is an intentionally placed bug here: != should be =
            cursor.execute("delete from Person where PersonID = %s", (personID,))
        self.connection.commit()