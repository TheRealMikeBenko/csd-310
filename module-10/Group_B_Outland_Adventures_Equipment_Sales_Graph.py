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

    # SQL query for equipment sales per customer
    query = """
    SELECT 
        Customers.customer_id,
        CONCAT(Customers.first_name, ' ', Customers.last_name) AS customer_name,
        COUNT(Equipment_Sales.sale_id) AS number_of_sales,
        SUM(Equipment_Sales.sale_quantity) AS total_purchases
    FROM Customers
    LEFT JOIN Equipment_Sales ON Customers.customer_id = Equipment_Sales.customer_id
    GROUP BY Customers.customer_id, customer_name
    ORDER BY Customers.customer_id;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Convert results to a DataFrame for graphing
    df = pd.DataFrame(results, columns=[
        "customer_id",
        "customer_name",
        "number_of_sales",
        "total_purchases"
    ])

    print("\n" + "*" * 50)
    print("EQUIPMENT SALES")
    print("*" * 50)

    for _, row in df.iterrows():
        print(f"Customer ID: {row['customer_id']}")
        print(f"Customer Name: {row['customer_name']}")
        print(f"Number of Sales: {row['number_of_sales']}")
        print(f"Total Purchases: {row['total_purchases']}")
        print("-" * 50)

    # Create a bar chart of total purchases per customer
    plt.bar(df["customer_name"], df["total_purchases"])
    plt.title("Equipment Purchases Per Customer")
    plt.xlabel("Customer")
    plt.ylabel("Total Purchases")
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