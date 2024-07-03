import subprocess

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
        






