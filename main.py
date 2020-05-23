from dbUtil import DatabaseUtils

class Menu:
    def main(self):
        with DatabaseUtils() as db:
            db.createBookingsTable()
        self.runMenu()

    def runMenu(self):
        while(True):
            print()
            print("1. List Users")
            print("2. List Cars")
            print("3. Insert User")
            print("4. Delete User")
            print("5. Insert Car")
            print("6. Delete Car")
            print("7. Drop table")
            print("8. Quit")
            selection = input("Select an option: ")
            print()

            if(selection == "1"):
                self.listPeople()
            elif(selection == "2"):
                self.listCars()
            elif(selection == "3"):
                self.insertPerson()
            elif(selection == "4"):
                self.deletePerson()
            elif(selection == "5"):
                self.insertCar()
            elif(selection == "6"):
                self.deleteCar()
            elif(selection == "7"):
                #print("Have to change dbUtil if you want to drop a table")
                self.dropTable()
            elif(selection == "8"):
                print("Goodbye!")
                break
            else:
                print("Invalid input - please try again.")

    def listPeople(self):
        print("--- People ---")
        print("{:<15} {}".format("Person ID", "Name"))
        with DatabaseUtils() as db:
            for person in db.getPeople():
                print("{:<15} {}".format(person[0], person[1]))
        
    def listCars(self):
        print("--- Cars ---")
        print("{:<15} {}".format("carId", "Make"))
        with DatabaseUtils() as db:
            for person in db.getCars():
                #print("{:<15} {}".format(person[0]))
                print(person)
                
    def dropTable(self):
        print("----Drop Table----")
        with DatabaseUtils() as db:
            if(db.dropTable()):
                print("dropped successfully.")
            else:
                print("didn't drop.")

    def insertPerson(self):
        print("--- Insert Person ---")
        name = input("Enter the person's name: ")
        with DatabaseUtils() as db:
            if(db.insertPerson(name)):
                print("{} inserted successfully.".format(name))
            else:
                print("{} failed to be inserted.".format(name))
    
    def deletePerson(self):
        print("--- Delete Person ---")
        id = input("Enter the person's ID: ")
        with DatabaseUtils() as db:
            if(db.deletePerson(id)):
                print("{} deleted successfully.".format(id))
            else:
                print("{} failed to delete user.".format(id))
    
    def insertCar(self):
        print("--- Insert Car ---")
        carId = input("Enter the car's id: ")
        make = input("Enter the car's make: ")
        body = input("Enter the car's body type: ")
        colour = input("Enter the car's colour: ")
        seats = input("Enter the car's seat number: ")
        location = input("Enter the car's location: ")
        cost = input("Enter the car's cost per hour: ")
        bookedBy = input("Enter the car's current owner, blank if no one: ")
        
        with DatabaseUtils() as db:
            if(db.insertCar(carId, make, body, colour, seats, location, cost, bookedBy)):
                print("{} inserted successfully.".format(make))
            else:
                print("{} failed to be inserted.".format(make))
    
    def deleteCar(self):
        print("--- Delete Car ---")
        id = input("Enter the car's ID: ")
        with DatabaseUtils() as db:
            if(db.deleteCar(id)):
                print("{} deleted successfully.".format(id))
            else:
                print("{} failed to delete car.".format(id))
    

if __name__ == "__main__":
    Menu().main()
