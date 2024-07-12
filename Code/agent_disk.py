import subprocess

result, commande = [],["(Get-Volume -DriveLetter C | Select-Object -ExpandProperty SizeRemaining) / 1GB", "(Get-Volume -DriveLetter C | Select-Object -ExpandProperty Size) / 1GB"]

def disk():
  process = subprocess.Popen(["powershell", "-Command", "hostname"], stdout=subprocess.PIPE)
  output, _ = process.communicate()
  result.append(output.decode("utf-8").split("\r")[0])

  for i in range(len(commande)):
    process = subprocess.Popen(["powershell", "-Command", commande[i]], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    result.append(float(output.decode("utf-8").split("\r")[0].replace(',', '.')))  
  result.append(result[2]-result[1])

  return result
