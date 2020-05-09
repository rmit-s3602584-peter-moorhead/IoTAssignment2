from dbUtil import DatabaseUtils

class Menu:
    def main(self):
        with DatabaseUtils() as db:
            db.createPersonTable()
        self.runMenu()

    def runMenu(self):
        while(True):
            print()
            print("1. List People")
            print("2. Insert Person")
            print("3. Delete Person")
            print("4. Drop table")
            print("5. Quit")
            selection = input("Select an option: ")
            print()

            if(selection == "1"):
                self.listPeople()
            elif(selection == "2"):
                self.insertPerson()
            elif(selection == "3"):
                self.deletePerson()
            elif(selection == "4"):
                self.dropTable()
            elif(selection == "5"):
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

if __name__ == "__main__":
    Menu().main()
