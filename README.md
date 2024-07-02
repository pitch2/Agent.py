Ce script en python permet de récolter des informations et de les envoyer vers une BDD. Il récolte les informations en PowerShell.

```powershell
Get-WmiObject -Class Win32_DiskDrive
```
Ici on liste toutes nos informations disponible (beaucoup)
![](https://raw.githubusercontent.com/pitch2/Agent.py/base/PsAgent-20240702221335274.webp)

Pour avoir un résultat intéressant on renvoie seulement ce dont l'on a besoin
```powershell
Get-WmiObject -Class Win32_DiskDrive | Select-Object -Property Model -Unique | Format-Table -HideTableHeaders
```
![](https://raw.githubusercontent.com/pitch2/Agent.py/base/PsAgent-20240702221413698.webp)

Nous avons de la pollution avec des sauts de lignes... Donc ->
```python
(((output.decode("utf-8").split("\r"))[1]).split("\n"))[1]
```


On crée notre table SQL pour prendre les données : 
```sql
CREATE TABLE IF NOT EXISTS `table_1` (
  `Hostname` varchar(255) NOT NULL,
  `Win32_Processor` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `Win32_PhysicalMemory` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `Win32_BaseBoard` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `Win32_DiskDrive` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`Hostname`)
) ENGINE=InnoDB;
```

Nous avons donc ça comme résultat:
![](https://raw.githubusercontent.com/pitch2/Agent.py/base/PsAgent-20240702224846587.webp)

Deux noms de PC ne peuvent pas être identique : 
![](https://raw.githubusercontent.com/pitch2/Agent.py/base/PsAgent-20240702224955420.webp)

Sur un parc informatique c'est normalement basique



3h - Adrien Pichon
