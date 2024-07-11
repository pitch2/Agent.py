import subprocess

def hardware():
  #Informations que nous voulons récupérer (voir note pour comprendre)
  
  dictionnaire_demande, colonne_type, hardware_dico = {
      "Win32_Processor": ["Name"],
      "Win32_VideoController": ["VideoProcessor"],
      "Win32_PhysicalMemory": ["__PROPERTY_COUNT"],
      "Win32_BaseBoard": ["Product"],
      "Win32_DiskDrive": ["Model", "Size", "Status"]
  }, ['Hostname','CPU','GPU','RAM','BaseBoard','DiskDrive_Model','DiskDrive_Size','DiskDrive_State'], {}

  # Récupération des informations du PC en Powershell
  # Récupération du nom de la machine

  process = subprocess.Popen(["powershell", "-Command", "hostname"], stdout=subprocess.PIPE)
  output, _ = process.communicate()
  hardware_dico["Hostname"] = (output.decode("utf-8").split("\r")[0])

  r = 1
  # Récupération des informations du dico
  for classe, proprietes in dictionnaire_demande.items():
      for propriete in proprietes:
        command = f"Get-WmiObject -Class {classe} | Select-Object -Property {propriete} -Unique | Format-Table -HideTableHeaders"
        # Exécuter la commande PowerShell et capturer la sortie
        process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE)

        # Décoder la sortie et l'afficher
        output, _ = process.communicate()

        lines = output.decode("utf-8").strip().split('\r\n')
        if len(lines) > 0:
            hardware_dico[colonne_type[r]] = lines[0].strip()

        r += 1

  return hardware_dico


