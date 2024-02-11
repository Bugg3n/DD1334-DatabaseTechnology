import sqlite3
from tkinter import HORIZONTAL
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Hypthesis

# Is there a connection between how far north / south a city is and the distribution of its industry?
# Usually richer countries has more services and industries while poorer countries rely more on agriculture. 

class Program:
    def __init__(self):
        self.connection1 = sqlite3.connect('mondial.db') # establish database connection
        self.cursor1 = self.connection1.cursor() # create a database query cursor
        self.cursor2 = self.connection1.cursor()
        self.cursor3 = self.connection1.cursor()
        self.actions = [self.scatterLatitudeEconomy, self.scatterAVG, self.averageInRange, self.exit]
        self.menu = ["Scatter plot Longitude vs economy", "Scatter plot average", "Average in specific range", "Exit"]

    def print_menu(self):
        for i,x in enumerate(self.menu):
            print("%i. %s"%(i+1,x))
        return self.get_int()

    def get_int(self):
        while True:
            try:
                choice = int(input("Choose: "))
                if 1 <= choice <= len(self.menu):
                    return choice
                print("Invalid choice.")
            except (NameError,ValueError, TypeError,SyntaxError):
                print("That was not a number, genious.... :(")


    def drop(self, name):
        # delete the table XYData if it does already exist
        try:
            query = "DROP TABLE " + name
            self.cursor1.execute(query)
            self.connection1.commit()  
            # by default in pgdb, all executed queries for connection 1 up to here form a transaction
            # we can also explicitly start tranaction by executing BEGIN TRANSACTION
        except sqlite3.Error as e:
            print("ROLLBACK: PopData table does not exists or other error.")
            print("Error message:", e.args[0])
            self.connection1.rollback()
            pass

    def query(self, query, cursor):
        print("U1: (start) " + query)
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            self.connection1.commit()
            return data
        except sqlite3.Error as e:
            print("Fel")
            print("Error message:", e.args[0])
            self.connection1.rollback()
            exit()           


    def close(self):
        self.connection1.close()

    def exit(self):
        self.cursor1.close()
        self.cursor2.close()
        self.cursor3.close()
        self.connection1.close()
        exit()

    def run(self):
        while True:
            try:
                self.actions[self.print_menu()-1]()
            except IndexError:
                print("INDEX ERROR")
                continue

    def scatterLatitudeEconomy(self):
        data = self.query("Select latitude, agriculture from popdata", self.cursor1)
        x_agriculture= []
        y_agriculture= []
        for r in data:
            if (r[0]!=None and r[1]!=None):
                x_agriculture.append(float(r[0]))
                y_agriculture.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        data = self.query("Select latitude, service from popdata", self.cursor1)
        x_services= []
        y_services= []
        for r in data:
            if (r[0]!=None and r[1]!=None):
                x_services.append(float(r[0]))
                y_services.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        data = self.query("Select latitude, industry from popdata", self.cursor1)
        x_industry= []
        y_industry= []
        for r in data:
            if (r[0]!=None and r[1]!=None):
                x_industry.append(float(r[0]))
                y_industry.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        plt.scatter(x_industry, y_industry, color = 'orange')
        plt.scatter(x_agriculture, y_agriculture, color = 'red')
        plt.scatter(x_services, y_services, color = 'blue')
        plt.title("Red = agriculture, blue = services, orange = industry")
        plt.savefig("figure.png") # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out

    def scatterAVG(self):
        while True:
            try:
                type = input("1: Agriculture\n2: Industry\n3: Services")
                if type == "1":
                    type = "Agriculture"
                    break
                elif type == "2":
                    type = "Industry"
                    break
                elif type == "3":
                    type = "Service"
                    break
                else:
                    print("It has to be a number between 1 and 3")
            except sqlite3.Error as e:
                print("Error message:", e.args[0])
        
        data = self.query("Select latitude, AVG(" + type + ") from popdata Group By latitude", self.cursor1)
        x_agriculture= []
        y_agriculture= []
        for r in data:
            if (r[0]!=None and r[1]!=None):
                x_agriculture.append(float(r[0]))
                y_agriculture.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        plt.scatter(x_agriculture, y_agriculture, color = 'red')
        plt.title("Red = agriculture, blue = services, orange = industry")
        plt.savefig("figure.png") # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out

    def averageInRange(self):
        while True:
            try:
                lowerBound = input("Latitude Lower bound: ")
                break
            except sqlite3.Error as e:
                print("Error message:", e.args[0])

        while True:
            try:
                upperBound = input("Latitude Upper bound: ")
                break
            except sqlite3.Error as e:
                print("Error message:", e.args[0])
        while True:
            try:
                type = input("1: Agriculture\n2: Industry\n3: Services\n")
                if type == "1":
                    type = "Agriculture"
                    break
                elif type == "2":
                    type = "Industry"
                    break
                elif type == "3":
                    type = "Service"
                    break
                else:
                    print("It has to be a number between 1 and 3")
            except sqlite3.Error as e:
                print("Error message:", e.args[0])
        result = (self.query("SELECT AVG(" + type + ") FROM popData WHERE latitude <= "+ upperBound + " AND latitude >= " + lowerBound, self.cursor1))
        if result[0][0] == None:
            print("No valid data")
        else: 
            print (type + " AVG: " + str(int(result[0][0])) + "%")

if __name__ == "__main__":
    db = Program()
    db.run()