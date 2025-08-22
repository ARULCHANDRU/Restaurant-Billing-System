# utils/db_utils.py

import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'restaurant.db')

def init_db():
    # ... (code from before, no changes here)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu (...)
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (...)
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (...)
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def populate_menu_from_csv(csv_path):
    # ... (code from before, no changes here)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        menu_df = pd.read_csv(csv_path)
        for index, row in menu_df.iterrows():
            cursor.execute('''
                INSERT OR IGNORE INTO menu (item_name, category, price, gst_percentage)
                VALUES (?, ?, ?, ?)
            ''', (row['item_name'], row['category'], row['price'], row['gst_percentage']))
        conn.commit()
    except (sqlite3.Error, pd.errors.EmptyDataError, KeyError) as e:
        print(f"An error occurred while populating the menu: {e}")
    finally:
        if conn:
            conn.close()

def get_menu():
    # ... (code from before, no changes here)
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu ORDER BY category, item_name")
        menu_items = cursor.fetchall()
        return [dict(row) for row in menu_items]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()

# --- NEW FUNCTION TO ADD ---
def save_order(order_details, items):
    """
    Saves a completed order to the 'orders' and 'order_items' tables.
    This is a transactional function.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Step 1: Insert into the main 'orders' table
        cursor.execute('''
            INSERT INTO orders (order_type, payment_method, subtotal, gst_amount, discount_percentage, grand_total)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            order_details['order_type'],
            order_details['payment_method'],
            order_details['subtotal'],
            order_details['total_gst'],
            order_details['discount_percentage'],
            order_details['grand_total']
        ))
        
        # Get the ID of the order we just inserted
        order_id = cursor.lastrowid

        # Step 2: Insert each item into the 'order_items' table
        for item in items:
            cursor.execute('''
                INSERT INTO order_items (order_id, item_id, quantity, price_per_item)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item['item_id'], item['quantity'], item['price']))

        conn.commit()
        print(f"Successfully saved order {order_id} to the database.")
        return order_id

    except sqlite3.Error as e:
        print(f"Database error during order save: {e}")
        return None
    finally:
        if conn:
            conn.close()

# Add these two new functions to the end of utils/db_utils.py

def get_all_orders():
    """Fetches all records from the orders and order_items tables."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # A complex query to join orders, order_items, and menu tables
        query = """
            SELECT
                o.order_id,
                o.order_date,
                o.grand_total,
                m.item_name,
                oi.quantity,
                m.category
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN menu m ON oi.item_id = m.item_id
            ORDER BY o.order_date DESC
        """
        cursor.execute(query)
        orders = cursor.fetchall()
        return [dict(row) for row in orders]

    except sqlite3.Error as e:
        print(f"Database error while fetching all orders: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_order_summary():
    """Fetches a summarized view of all orders."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query to get high-level order details
        query = "SELECT order_id, order_date, grand_total, payment_method FROM orders ORDER BY order_date DESC"
        cursor.execute(query)
        summary = cursor.fetchall()
        return [dict(row) for row in summary]

    except sqlite3.Error as e:
        print(f"Database error while fetching order summary: {e}")
        return []
    finally:
        if conn:
            conn.close()