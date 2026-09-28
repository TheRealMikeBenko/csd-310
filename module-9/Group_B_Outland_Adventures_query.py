# Group B
# Michael Benko, Michael Gordon, and Jacob Richman
# 2026-09-27
# CSD310-302E Database Development and Use (2267-DD)
# Module 9.1 Milestone #2

""" import statements """
import mysql.connector
from mysql.connector import errorcode
 
import dotenv
from dotenv import dotenv_values
 
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
 
 
def show_table(cursor, table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
 
    results = cursor.fetchall()
 
    # Get column names
    columns = cursor.column_names
 
    print('\n' + '*' * 50)
    print(table_name.upper())
    print('*' * 50)
 
    # Show each row
    for row in results:
        for labels in range(len(columns)):
            # Column name formatting
            label = columns[labels].replace('_', ' ').title()
            print(f'{label}: {row[labels]}')
 
        print('-' * 50)
 
 
try:
    db = mysql.connector.connect(**config)  # Connect to the Outland Adventures database
    # Create cursor
    cursor = db.cursor()
 
    # Show data from each table
    show_table(cursor, 'Roles')
    show_table(cursor, 'Customers')
    show_table(cursor, 'Address')
    show_table(cursor, 'Locations')
    show_table(cursor, 'Categories')
    show_table(cursor, 'Employees')
    show_table(cursor, 'Trips')
    show_table(cursor, 'Bookings')
    show_table(cursor, 'Equipment')
    show_table(cursor, 'Equipment_Rentals')
    show_table(cursor, 'Equipment_Sales')
 
 
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