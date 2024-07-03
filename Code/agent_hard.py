import subprocess
import mysql.connector


#Connexion à la BDD
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="agent"
)



#Informations que nous voulons récupérer (voir note pour comprendre)
dictionnaire, liste = {
    "Win32_Processor": ["Name"],
    "Win32_VideoController": ["VideoProcessor"],
    "Win32_PhysicalMemory": ["__PROPERTY_COUNT"],
    "Win32_BaseBoard": ["Product"],
    "Win32_DiskDrive": ["Model", "Size", "Status"]
}, []

# Récupération des informations du PC en Powershell
# Récupération du nom de la machine

process = subprocess.Popen(["powershell", "-Command", "hostname"], stdout=subprocess.PIPE)
output, _ = process.communicate()
liste.append(output.decode("utf-8").split("\r")[0])

# Récupération des informations du dico
for classe, proprietes in dictionnaire.items():
    for propriete in proprietes:
      command = f"Get-WmiObject -Class {classe} | Select-Object -Property {propriete} -Unique | Format-Table -HideTableHeaders"
      # Exécuter la commande PowerShell et capturer la sortie
      process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE)

      # Décoder la sortie et l'afficher
      output, _ = process.communicate()

      #print((((output.decode("utf-8").split("\r"))[1]).split("\n"))[1])
      liste.append((((output.decode("utf-8").split("\r"))[1]).split("\n"))[1])

print(liste)
    


# Envoie des données vers la BDD
mycursor = mydb.cursor()
sql = "INSERT INTO Hardware (Hostname, CPU, GPU, RAM, BaseBoard, DiskDrive_Model, DiskDrive_Size, DiskDrive_State) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
val = (liste[0], liste[1], liste[2], liste[3], liste[4], liste[5], liste[6], liste[7])
mycursor.execute(sql, val)
mydb.commit()


print(mycursor.rowcount, "Validé")




