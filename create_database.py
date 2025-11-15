import sqlite3


# Here we are creating a dummy database 

conn = sqlite3.connect('amazon.db')
cursor = conn.cursor()

# Creating tables

# Tables : customers , orders , products , order_items

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    city TEXT,
    join_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    stock INTEGER,
    category TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT,
    status TEXT,
    total_amount REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);
""")



# Enter dummy data

