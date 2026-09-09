# Michael Benko
# 2026-09-9
# CSD310-302E Database Development and Use (2267-DD)
# Module 6.2 Assignment

""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode
 
import dotenv # to use .env file
from dotenv import dotenv_values

#using our .env file
secrets = dotenv_values(".env")
 
""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

try:
    """ try/catch block for handling potential MySQL database errors """ 
 
    db = mysql.connector.connect(**config) # connect to the movies database
    cursor = db.cursor()

    # output the connection status 
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    print("\n-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT * FROM studio")
    studios = cursor.fetchall()
    for studio in studios:
        print("Studio ID: {}\nStudio Name: {}\n".format(studio[0], studio[1]))

    print("\n-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT * FROM genre")
    genres = cursor.fetchall()
    for genre in genres:
        print("Genre ID: {}\nGenre Name: {}\n".format(genre[0], genre[1]))

    print("\n-- DISPLAYING Short Film RECORDS --")
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
    short_films = cursor.fetchall()
    for film in short_films:
        print("Film Name: {}\nRuntime: {}\n".format(film[0], film[1]))

    print("\n-- DISPLAYING Director RECORDS in Order --")
    cursor.execute("SELECT film_director, film_name FROM film ORDER BY film_director")
    films_by_director = cursor.fetchall()
    for film in films_by_director:
        print("Director: {}\nFilm Name: {}\n".format(film[0], film[1]))
    
    input("\n\n  Press any key to continue...")
 
except mysql.connector.Error as err:
    """ on error code """
 
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
 
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
 
    else:
        print(err)

finally:
    """ close the connection to MySQL """
 
    db.close()