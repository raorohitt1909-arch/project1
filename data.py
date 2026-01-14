import pandas as pd
import random
from faker import Faker

fake = Faker()

data = []

products = ["Laptop", "Phone", "Headphones", "Camera", "Shoes", "Watch", "TV"]
categories = ["Electronics", "Fashion"]
regions = ["North", "South", "East", "West"]

for i in range(1, 100001):
    data.append([
        i,
        fake.date_between(start_date='-2y', end_date='today'),
        random.randint(1000, 1100),
        fake.name(),
        random.choice(products),
        random.choice(categories),
        random.randint(1, 5),
        random.randint(500, 50000),
        random.choice(regions)
    ])

columns = ["order_id","order_date","customer_id","customer_name",
           "product","category","quantity","price","region"]

df = pd.DataFrame(data, columns=columns)
df.to_csv("sales_data.csv", index=False)

print("sales_data.csv created with 100,000 rows")



import pandas as pd

df = pd.read_csv("sales_data.csv")

# Remove nulls
df.dropna(inplace=True)

# Fix data types
df['order_date'] = pd.to_datetime(df['order_date'])
df['quantity'] = df['quantity'].astype(int)
df['price'] = df['price'].astype(float)

# Remove negative or zero price
df = df[df['price'] > 0]

print("Cleaning done")


# New column
df['total_sales'] = df['quantity'] * df['price']
df['month'] = df['order_date'].dt.month
df['year'] = df['order_date'].dt.year

# Save cleaned data
df.to_csv("clean_sales.csv", index=False)

print("Transformation done & saved")



import pandas as pd
import mysql.connector

df = pd.read_csv("clean_sales.csv")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abc123@",   # change
    database="sales_dbb"
)

cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO sales_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, tuple(row))

conn.commit()
print("Data inserted successfully")

cursor.close()
conn.close()



import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abc123@",
    database="sales_dbb"
)

# Product sales
df = pd.read_sql("SELECT product, SUM(total_sales) revenue FROM sales_data GROUP BY product", conn)

plt.figure()
plt.bar(df['product'], df['revenue'])
plt.title("Product Sales")
plt.xticks(rotation=45)
plt.show()

# Monthly trend
df2 = pd.read_sql("""
SELECT CONCAT(year,'-',month) ym, SUM(total_sales) revenue
FROM sales_data GROUP BY ym ORDER BY ym
""", conn)

plt.figure()
plt.plot(df2['ym'], df2['revenue'])
plt.xticks(rotation=90)
plt.title("Monthly Sales Trend")
plt.show()

# Category pie
df3 = pd.read_sql("SELECT category, SUM(total_sales) revenue FROM sales_data GROUP BY category", conn)

plt.figure()
plt.pie(df3['revenue'], labels=df3['category'], autopct='%1.1f%%')
plt.title("Category Contribution")
plt.show()

conn.close()




