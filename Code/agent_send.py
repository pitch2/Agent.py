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
hardware_dico, network_dico = agent_hard.hardware(), agent_net.network()

#Envoie des données de Hardware
mycursor = mydb.cursor()
sql = "INSERT INTO Hardware (Hostname, CPU, GPU, RAM, BaseBoard, DiskDrive_Model, DiskDrive_Size, DiskDrive_State) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
val = (
    hardware_dico['Hostname'],
    hardware_dico['CPU'],
    hardware_dico['GPU'],
    hardware_dico['RAM'],
    hardware_dico['BaseBoard'],
    hardware_dico['DiskDrive_Model'],
    hardware_dico['DiskDrive_Size'],
    hardware_dico['DiskDrive_State']
)

mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "Validé")

#Envoie des données de Network
mycursor = mydb.cursor()
sql = "INSERT INTO Network (Hostname, Domain, SerialNumber, Bios_Releasedate) VALUES (%s, %s, %s, %s)"
val = (
    network_dico['Hostname'],
    network_dico['Domain'],
    network_dico['SerialNumber'],
    network_dico['Bios_Releasedate'],
)

mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "Validé")
