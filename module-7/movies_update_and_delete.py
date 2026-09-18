# Michael Benko
# 2026-09-18
# CSD310-302E Database Development and Use (2267-DD)
# Module 7.2 Assignment

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

def show_films (cursor, title):
    # method to execute an inner join on all tables,
    # iterate over the dataset and output the results to the terminal window.
 
    # inner join query
    cursor.execute("select film_name as Name, film_director as Director, genre_name as Genre, studio_name as 'Studio Name' from film INNER JOIN genre ON film.genre_id=genre.genre_id INNER JOIN studio ON film.studio_id=studio.studio_id")
    
    # get the results from the cursor object
    films = cursor.fetchall()
 
    # output the results
    print("\n  -- {} --".format(title))
 
    # iterate over the film data set and display the results
    for film in films:
        print("Film Name: {}\n  Director: {}\n  Genre Name: {}\n  Studio Name: {}\n".format(film[0], film[1], film[2], film[3]))

try:
    """ try/catch block for handling potential MySQL database errors """ 
 
    db = mysql.connector.connect(**config) # connect to the movies database
    cursor = db.cursor()

    # output the connection status 
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    # Showing films
    show_films(cursor, "DISPLAYING FILMS")

    # Inserting a film
    cursor.execute("INSERT INTO film (film_name, film_director, film_releaseDate, film_runtime, genre_id, studio_id) VALUES ('Cast Away', 'Robert Zemeckis', 2000, 143, 3, 1)")
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # Updating a film
    cursor.execute("UPDATE film SET genre_id = 1 WHERE film_name = 'Alien'")
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

    # Deleting a film
    cursor.execute("DELETE FROM film WHERE film_name = 'Gladiator'")
    db.commit()
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")
 
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