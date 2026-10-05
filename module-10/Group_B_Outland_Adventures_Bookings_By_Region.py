# Group B
# Michael Benko, Michael Gordon, and Jacob Richman
# 2026-10-3
# CSD310-302E Database Development and Use (2267-DD)
# Module 10.1 Milestone #3

""" import statements """
import mysql.connector
from mysql.connector import errorcode

import dotenv
from dotenv import dotenv_values

import pandas as pd
import matplotlib.pyplot as plt

# Using the .env file
secrets = dotenv_values(".env")

# Database config object
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

# Report needs to answer:
# So far, they have conducted treks in Africa, Asia, and Southern Europe.
# Is there any one of those locations that has a downward trend in bookings?
 
def booking_data(cursor, table_name):
 
    # Get data for Bookings, Locations, and Trips. Group by location with a count of each booking per location, per year
    # Use alias for booking_date and the count of booking_ids for report formatting
    cursor.execute(f'SELECT Locations.Location_Name, YEAR(Bookings.Booking_Date) AS Booking_Year, COUNT(Bookings.Booking_ID) AS Total_Bookings '
                   'FROM Bookings '
                   'JOIN Trips ON Bookings.Trip_ID = Trips.Trip_ID '
                   'JOIN Locations ON Trips.Location_ID = Locations.Location_ID '
                   'GROUP BY Locations.Location_Name, YEAR(Bookings.Booking_Date) '
                   'ORDER BY Locations.Location_Name, Booking_Year;')
 
    results = cursor.fetchall()
 
    print('\n' + '*' * 50)
    print('BOOKING TREND REPORT')
    print('*' * 50)
 
    # Create a variable for the current location to use in the loop
    current_location = ''
 
    # Show each row
    for row in results:
        location = row[0]
        year = row[1]
        total = row[2]
 
        # Print data out but only print location if it changes
        if location != current_location:
            print(f'\nLocation: {location}')
            print('Booking Year      Total Bookings')
            print('-' * 35)
 
            current_location = location
 
        # Print out booking year and total bookings < left justified 18 spaces
        print(f'{year:<18}{total}')
 
        # print('-' * 35)
    print()
 
 
try:
    db = mysql.connector.connect(**config)  # Connect to the database
    # Create cursor
    cursor = db.cursor()
 
    booking_data(cursor, 'Bookings')
 
 
except mysql.connector.Error as err:
    # On error code
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)
finally:
    # Close the connection
    db.close()