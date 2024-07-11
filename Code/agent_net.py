import subprocess

def network():
    # Informations que nous voulons récupérer (voir note pour comprendre)
    dictionnaire, colonne_type, network_dico = {
        "Win32_computersystem": ["Domain"],
        "Win32_BIOS": ["SerialNumber", "ReleaseDate"]
    },['Hostname', 'Domain', 'SerialNumber', 'Bios_Releasedate'],{}

    # Récupération des informations du PC en Powershell
    # Récupération du nom de la machine
    process = subprocess.Popen(["powershell", "-Command", "hostname"], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    network_dico["Hostname"] = output.decode("utf-8").strip()

    r = 1
    # Récupération des informations du dico
    for classe, proprietes in dictionnaire.items():
        for propriete in proprietes:
            command = f"Get-WmiObject -Class {classe} | Select-Object -Property {propriete} -Unique | Format-Table -HideTableHeaders"
            # Exécuter la commande PowerShell et capturer la sortie
            process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE)

            # Décoder la sortie et l'afficher
            output, _ = process.communicate()

            # formater nos informations de la bonne façon
            lines = output.decode("utf-8").strip().split('\r\n')
            if len(lines) > 0:
                network_dico[colonne_type[r]] = lines[0].strip()
            r += 1

    return network_dico
