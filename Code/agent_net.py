import subprocess
import mysql.connector


#Connexion à la BDD
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="agent"
)


def network ():
    #Informations que nous voulons récupérer (voir note pour comprendre)
    dictionnaire, liste = {
        "Win32_computersystem": ["Domain"],
        "Win32_BIOS": ["SerialNumber", "releasedate"],
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

            #formater nos informations de la bonne façon
            liste.append((((output.decode("utf-8").split("\r"))[1]).split("\n"))[1])

    return liste
        

network_liste = network()

# Envoie des données vers la BDD
mycursor = mydb.cursor()
sql = "INSERT INTO Network (Hostname, Domain, SerialNumber, Bios_Releasedate) VALUES (%s, %s, %s, %s)"
val = (network_liste[0], network_liste[1], network_liste[2], network_liste[3])
mycursor.execute(sql, val)
mydb.commit()


print(mycursor.rowcount, "Validé")




