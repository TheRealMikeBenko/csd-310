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

try:
    db = mysql.connector.connect(**config)  # Connect to the Outland Adventures database
    cursor = db.cursor()

    # SQL query for inventory items older than 5 years
    query = """
    SELECT 
        equipment_id,
        equipment_name,
        purchase_date,
        TIMESTAMPDIFF(YEAR, purchase_date, CURDATE()) AS age_years
    FROM Equipment
    WHERE TIMESTAMPDIFF(YEAR, purchase_date, CURDATE()) > 5;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Convert results to a DataFrame for graphing
    df = pd.DataFrame(results, columns=[
        "equipment_id",
        "equipment_name",
        "purchase_date",
        "age_years"
    ])

    print("\n" + "*" * 50)
    print("INVENTORY ITEMS OVER FIVE YEARS OLD")
    print("*" * 50)

    for _, row in df.iterrows():
        print(f"Equipment ID: {row['equipment_id']}")
        print(f"Equipment Name: {row['equipment_name']}")
        print(f"Purchase Date: {row['purchase_date']}")
        print(f"Age (Years): {row['age_years']}")
        print("-" * 50)

    # Create a bar chart of equipment ages
    plt.bar(df["equipment_name"], df["age_years"])
    plt.title("Equipment Over Five Years Old")
    plt.xlabel("Equipment Name")
    plt.ylabel("Age (Years)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")
    else:
        print(err)
finally:
    db.close()