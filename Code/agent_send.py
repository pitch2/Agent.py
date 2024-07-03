import mysql.connector
import agent_hard
import agent_net


#Connexion à la BDD
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="agent"
)


# Création des listes avec les informations
hardware_liste = agent_hard.hardware()
network_liste = agent_net.network()

#Envoie des données de Hardware
mycursor = mydb.cursor()
sql = "INSERT INTO Hardware (Hostname, CPU, GPU, RAM, BaseBoard, DiskDrive_Model, DiskDrive_Size, DiskDrive_State) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
val = (hardware_liste[0], hardware_liste[1], hardware_liste[2], hardware_liste[3], hardware_liste[4], hardware_liste[5], hardware_liste[6], hardware_liste[7])
mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "Validé")



#Envoie des données de Network
mycursor = mydb.cursor()
sql = "INSERT INTO Network (Hostname, Domain, SerialNumber, Bios_Releasedate) VALUES (%s, %s, %s, %s)"
val = (network_liste[0], network_liste[1], network_liste[2], network_liste[3])
mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "Validé")
