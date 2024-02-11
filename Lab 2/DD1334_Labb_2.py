import sqlite3
from tkinter import HORIZONTAL
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

class Program:
    def __init__(self):
        self.connection1 = sqlite3.connect('mondial.db') # establish database connection
        self.cursor1 = self.connection1.cursor() # create a database query cursor
        self.cursor2 = self.connection1.cursor()
        self.cursor3 = self.connection1.cursor()
        self.actions = [self.scatterPlotPopulationQuery, self.scatterPlotPopulationQueryStockholm, self.scatterPlotPopulationSum, self.estimateCityPopulation, self.createLinearprediction, self.createPrediction, self.scatterPredictions, self.exit]
        self.menu = ["scatter plot all cities", "scatter plot Population of Stockholm", "scatter plot population sum per city", "Estimate city population", "Create Linear Prediction Table", "Create Prediction Table", "Scatter Plot of predictions", "Exit"]

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

    def scatterPlotPopulationQuery(self):
        data = self.query("Select year, population from PopData", self.cursor1)
        xs= []
        ys= []
        for r in data:
            # you access ith component of row r with r[i], indexing starts with 0
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            #print("Considering tuple", r)
            if (r[0]!=None and r[0]!=None):
                xs.append(float(r[0]))
                ys.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        # print("xs:", xs)
        # print("ys:", ys)
        plt.scatter(xs, ys)
        plt.title("Total population per year")
        plt.savefig("figure.png") # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out

    def scatterPlotPopulationQueryStockholm(self):
        data = self.query("Select year, population from PopDataStockholm", self.cursor1)
        xs= []
        ys= []
        for r in data:
            # you access ith component of row r with r[i], indexing starts with 0
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            # print("Considering tuple", r)
            if (r[0]!=None and r[0]!=None):
                xs.append(float(r[0]))
                ys.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        # print("xs:", xs)
        # print("ys:", ys)
        plt.scatter(xs, ys)
        plt.title("Population Stockholm per year")
        plt.savefig("figure.png") # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out

    def scatterPlotPopulationSum(self):
        data = self.query("Select year, SUM(population) from popData GROUP BY year", self.cursor1)
        xs= []
        ys= []
        for r in data:
            # you access ith component of row r with r[i], indexing starts with 0
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            # print("Considering tuple", r)
            if (r[0]!=None and r[0]!=None):
                xs.append(float(r[0]))
                ys.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        # print("xs:", xs)
        # print("ys:", ys)
        plt.scatter(xs, ys)
        plt.title("Total population sum per year")
        plt.savefig("figure.png") # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out

    def estimateCityPopulation(self):
        countryCode = input("Country Code: ")
        cityName = input("City:")
        data = self.query("Select year, population from popData WHERE country LIKE \"" + countryCode + "\" AND name LIKE \"" + cityName + "\"", self.cursor1)
        xs= []
        ys= []
        for r in data:
            # you access ith component of row r with r[i], indexing starts with 0
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            # print("Considering tuple", r)
            if (r[0]!=None and r[0]!=None):
                xs.append(float(r[0]))
                ys.append(float(r[1]))
            else:
                print("Dropped tuple ", r)

        x_train = np.array(xs).reshape([-1,1])
        x_test = np.array(xs).reshape([-1,1])
        y_train = np.array(ys).reshape([-1,1])
        y_test = np.array(ys).reshape([-1,1])
        regr = LinearRegression().fit(x_train, y_train)
        y_pred = regr.predict(x_test)
        score = regr.score(np.array(xs).reshape([-1,1]), np.array(ys).reshape([-1,1]))
        a = regr.coef_[0][0]
        b = regr.intercept_[0]

        plt.scatter(xs, ys)
        plt.plot(x_test, y_pred, color="blue", linewidth=3)   
        plt.title("City population and prediction for " + countryCode + ", " + cityName + ". a: " + str(a) + "b:" + str(b) + "score: "+ str(score))
        plt.xticks(())
        plt.yticks(())    
        plt.savefig("figure.png") # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out

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

    def createLinearprediction(self):
        # Drop table if it exists
        try:
            stmt = "SELECT * FROM 'linearprediction' LIMIT 1"
            self.cursor1.execute(stmt)
            self.drop("linearprediction")
        except:
            pass
        self.query("CREATE TABLE linearprediction(name VARCHAR2(50) NOT NULL, country VARCHAR2(4) NOT NULL, a float NOT NULL, b float NOT NULL, score float NOT NULL CHECK(score >= 0 AND score <= 1))", self.cursor1)
        self.cursor1.execute("SELECT DISTINCT country from PopData")
        for country in self.cursor1:
            self.cursor2.execute("SELECT DISTINCT name FROM popData WHERE country LIKE '" + country[0] + "'")
            for city in self.cursor2:
                data = self.query("Select year, population from popData WHERE country LIKE \"" + country[0] + "\" AND name LIKE \"" + city[0] + "\"", self.cursor3)
                xs= []
                ys= []
                for r in data:
                    # you access ith component of row r with r[i], indexing starts with 0
                    # check for null values represented as "None" in python before conversion and drop
                    # row whenever NULL occurs
                    # print("Considering tuple", r)
                    if (r[0]!=None and r[0]!=None):
                        xs.append(float(r[0]))
                        ys.append(float(r[1]))
                    else:
                        print("Dropped tuple ", r)

                x_train = np.array(xs).reshape([-1,1])
                x_test = np.array(xs).reshape([-1,1])
                y_train = np.array(ys).reshape([-1,1])
                y_test = np.array(ys).reshape([-1,1])
                regr = LinearRegression().fit(x_train, y_train)
                y_pred = regr.predict(x_test)
                score = regr.score(np.array(xs).reshape([-1,1]), np.array(ys).reshape([-1,1]))
                a = regr.coef_[0][0]
                b = regr.intercept_[0]
                query = "INSERT INTO linearprediction VALUES (\"" + city[0] + "\", \"" + country[0] + "\", '" + str(a) + "', '" + str(b) + "', '" +  str(score) + "')"
                try:
                    self.cursor3.execute(query)
                    self.connection1.commit()
                except sqlite3.Error as e: 
                    print("Error message:", e.args[0])
                    pass
        print(self.query("SELECT * FROM linearprediction limit 5", self.cursor1))

    def createPrediction(self):
        try:
            stmt = "SELECT * FROM 'linearprediction' LIMIT 1"
            self.cursor1.execute(stmt)
            self.drop("prediction")
        except:
            pass
        self.query("CREATE TABLE prediction (name VARCHAR2(50), country VARCHAR2(4), population INT, year INT)", self.cursor1)
        for year in range (1950, 2050, 1):
            self.query("INSERT INTO prediction SELECT name, country, a*" + str(year) + "+b, " + str(year) + " FROM linearprediction", self.cursor1)
        # print(self.query("SELECT * FROM prediction limit 10", self.cursor1))
        # population = b + a*x

    def scatterPredictions(self):
        data = self.query("Select year, population from prediction", self.cursor1)
        xs= []
        ys= []
        for r in data:
            if (r[0]!=None and r[0]!=None):
                xs.append(float(r[0]))
                ys.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        data = self.query("Select year, AVG(population) from prediction GROUP BY year", self.cursor1)
        xs_avg= []
        ys_avg= []
        for r in data:
            if (r[0]!=None and r[0]!=None):
                xs_avg.append(float(r[0]))
                ys_avg.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        data = self.query("Select year, MAX(population) from prediction GROUP BY year", self.cursor1)
        xs_sum= []
        ys_sum= []
        for r in data:
            if (r[0]!=None and r[0]!=None):
                xs_sum.append(float(r[0]))
                ys_sum.append(float(r[1]))
            else:
                print("Dropped tuple ", r)
        plt.scatter(xs, ys)
        plt.scatter(xs_avg, ys_avg, color='red')
        plt.scatter(xs_sum, ys_sum, color='green')
        plt.title("Predicted population per year and city")
        plt.savefig("figure.png") # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out

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

if __name__ == "__main__":
    db = Program()
    db.run()