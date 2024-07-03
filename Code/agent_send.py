import mysql.connector

#Connexion à la BDD
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="agent"
)

