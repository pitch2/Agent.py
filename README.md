Ce script en python permet de récolter des informations et de les envoyer vers une BDD. Il récolte les informations en PowerShell.

```powershell
Get-WmiObject -Class Win32_DiskDrive
```
Ici on liste toutes nos informations disponible (beaucoup)
![](https://raw.githubusercontent.com/pitch2/Agent.py/base/Source/PsAgent-20240702221335274.webp)

Pour avoir un résultat intéressant on renvoie seulement ce dont l'on a besoin
```powershell
Get-WmiObject -Class Win32_DiskDrive | Select-Object -Property Model -Unique | Format-Table -HideTableHeaders
```
![](https://raw.githubusercontent.com/pitch2/Agent.py/base/Source/PsAgent-20240702221413698.webp)
Nous avons de la pollution avec des sauts de lignes... Donc ->
```python
(((output.decode("utf-8").split("\r"))[1]).split("\n"))[1]
```


On crée notre table SQL pour prendre les données : 
```sql
CREATE TABLE IF NOT EXISTS `Hardware` (

  `Hostname` varchar(255) NOT NULL,
  `CPU` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `GPU` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `RAM` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `BaseBoard` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `DiskDrive_Model` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `DiskDrive_Size` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `DiskDrive_State` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`Hostname`)
) ENGINE=InnoDB;
```

```sql
CREATE TABLE IF NOT EXISTS `Network` (
  `Hostname` VARCHAR(255) NOT NULL,
  `Domain` VARCHAR(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `SerialNumber` VARCHAR(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `Bios_Releasedate` VARCHAR(255) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`Hostname`)
) ENGINE=InnoDB;

```
Nous avons donc ça comme résultat
![](https://raw.githubusercontent.com/pitch2/Agent.py/base/Source/PsAgent-20240702224846587.webp)

Deux noms de PC ne peuvent pas être identique : 
![](https://raw.githubusercontent.com/pitch2/Agent.py/base/Source/PsAgent-20240702224955420.webp)

Sur un parc informatique c'est normalement basique



Faire une table pour partie réseau, hardware, organisation
- Réseau 
	- IP, MAC
- Hardware
	- CPU 
	- CM 
	- GPU 
	- RAM 
	- Etat des disques 
- Organisation
	- Numéro de série
	- Date du BIOS


---

Pour hardware : 
```python
dico = {
    "Win32_Processor" : "Name",
    "Win32_PhysicalMemory" : "__PROPERTY_COUNT",
    "Win32_BaseBoard" : "Product",
    "Win32_DiskDrive" : "Model",
	"Win32_DiskDrive" : "Size",
	"Win32_DiskDrive" : "Status",
	"Win32_VideoController" : "VideoProcessor",
	"Win32_OperatingSystem" : "Caption"
}
```

Pour organisation : 
```python
dico = {
	"Win32_computersystem" : "Domain",
	"Win32_BIOS" : "SerialNumber",
	"Win32_BIOS" : "releasedate"
}
```



3h - Adrien Pichon - V1
