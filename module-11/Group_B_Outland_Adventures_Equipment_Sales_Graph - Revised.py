# Group B
# Michael Benko, Michael Gordon, and Jacob Richman
# 2026-10-11
# CSD310-302E Database Development and Use (2267-DD)
# Module 11.2 Milestone #5

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
    # Connect to the Outland Adventures database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
 
    # SQL query for equipment sales by item
    query = """
    SELECT
        Equipment.equipment_name,
        COUNT(Equipment_Sales.sale_id) AS number_of_sales,
        SUM(Equipment_Sales.sale_quantity) AS total_quantity_sold
    FROM Equipment
    LEFT JOIN Equipment_Sales
        ON Equipment.equipment_id = Equipment_Sales.equipment_id
    GROUP BY Equipment.equipment_name
    ORDER BY Equipment.equipment_name;
    """
 
    cursor.execute(query)
    results = cursor.fetchall()
 
    # Convert results to a DataFrame for graphing
    df = pd.DataFrame(results, columns=[
        "equipment_name",
        "number_of_sales",
        "total_quantity_sold"
    ])
 
    print("\n" + "*" * 50)
    print("EQUIPMENT SALES BY ITEM")
    print("*" * 50)
 
    for _, row in df.iterrows():
        print(f"Equipment Name: {row['equipment_name']}")
        print(f"Number of Sales: {row['number_of_sales']}")
        print(f"Total Quantity Sold: {row['total_quantity_sold']}")
        print("-" * 50)
 
    # Create a bar chart of total purchases per equipment
    plt.bar(df["equipment_name"], df["total_quantity_sold"])
 
    goal = 3
 
    #     # Add a goal line for the graph
    plt.axhline(y=goal, linestyle='--', label='Goal: 3 purchases')
 
    plt.title("Equipment Sales by Item")
    plt.xlabel("Equipment Item")
    plt.ylabel("Total Quantity Sold")
    plt.yticks(range(0, int(df["total_quantity_sold"].max()) + 1))
    plt.xticks(rotation=45, ha="right")
 
    #     # Add legend so goal line explanation shows
    plt.legend()
 
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