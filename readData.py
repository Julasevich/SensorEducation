#SensorEd Workshop V0.2
#Author - Jacob Ulasevich
#Reading Data Introduction

"""
Gathering data is useless without being able to SEE what you are reading.
This program will take you through printing out the data of our sensor
database.
"""
import sqlite3
import os
from sqlite3 import Error

#Connect to the database file by specifying the path as the parameter
db = sqlite3.connect()

#Assign the curser to manage the database
cursor = db.cursor()

#Retrieve Data
cursor.execute('''SELECT dateTime, temperature, pressure, humidty, gas FROM <MAC ADDRESS>''')

#Declare a variable that will acquire all the data using cursor.fethchall()
all_rows = cursor.fetchall()

"""
Previosuly we learned about WHILE loops. To read this data we will be using a FOR loop.
In short, a for loop iterates over every item in a group.  For every item you will execute
one bit of code.
"""

"""
To format a print statement  you can put a {#} with # being the order it comes with after
the initial print statement. For example:
print("Hello {0}, ,my name is {1}'.format("Student", "Jacob"))
"""

for row in all_rows:
    #If row[0] Displays the date time, what do you think displays the other data? Format a print statement to display the data.
    

#Similar to cleaning up the GPIO, we have to commit and close the database. 
db.commit()
db.close()
