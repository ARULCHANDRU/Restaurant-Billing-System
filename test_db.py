# test_db.py
from utils import db_utils
import os

# Define the path to the menu csv file
CSV_FILE_PATH = os.path.join('data', 'menu.csv')

print("--- Starting Database Test ---")

# Step 1: Initialize the database and create tables
db_utils.init_db()

# Step 2: Populate the menu table from our CSV file
db_utils.populate_menu_from_csv(CSV_FILE_PATH)

print("\n--- Database Test Complete ---")
print(f"Please check your 'db' folder for the 'restaurant.db' file.")