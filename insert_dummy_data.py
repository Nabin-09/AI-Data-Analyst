from faker import Faker
import sqlite3
import random


fake = Faker()

conn = sqlite3.connect('amazon.db')
cursor = conn.cursor()

for _ in range(100):
    cursor.execute("""
        INSERT INTO customers (name , email , city , join_date)
        VALUES(? , ? , ? , ?)
        """ , (fake.name() , fake.email() , fake.city() , fake.date()))
    
# Insert 50 products

for _ in range(50):
    cursor.execute("""
    INSERT INTO products(name , price , stock , category)
    VALUES(? , ? , ? , ?)
    """ , (
        fake.word().capitalize(),
        round(random.uniform(10 , 500) , 2),
        random.randint(10 , 200),
        fake.word()
    ))

for _ in range(200):
    customer_id = random.randint(1 , 100)
    cursor.execute("""
    INSERT INTO orders(customer_id , order_date , status , total_amount)
    VALUES(? , ? , ? , ?)
""" , (customer_id , fake.date() , random.choice(['Pending' , 'Shipped' , 'Delivered']) , 0))
    
conn.commit()
conn.close()


print('Dummy data inserted successfully🚀!')