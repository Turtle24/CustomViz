import mysql.connector
import pandas as pd

# Open database connection
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="fear1234",
  database="stocks"
)

# prepare a cursor object using cursor  method
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM stocks")

myresult = mycursor.fetchall()

df = pd.read_sql("SELECT * FROM stocks", con=mydb)
df.head(5)
mydb.close()