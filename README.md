```powershell
Get-WmiObject -Class Win32_DiskDrive
```
Ici on liste toutes nos informations disponible (beaucoup)
![[PsAgent-20240702221335274.webp]]
Pour avoir un résultat intéressant on renvoie seulement ce dont l'on a besoin
```powershell
Get-WmiObject -Class Win32_DiskDrive | Select-Object -Property Model -Unique | Format-Table -HideTableHeaders
```
![[PsAgent-20240702221413698.webp]]
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

```sql
CREATE TABLE IF NOT EXISTS `disk` (
  `Hostname` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `Remaining` int DEFAULT NULL,
  `Total_Size` int DEFAULT NULL,
  `Buzy_Size` int DEFAULT NULL,
  PRIMARY KEY (`Hostname`)
) ENGINE=InnoDB;
```

Nous avons donc ça comme résultat
![[PsAgent-20240702224846587.webp]]

Deux noms de PC ne peuvent pas être identique : 
![[PsAgent-20240702224955420.webp]]
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

Pour calcul de disque exact : 
```python
commande = ["(Get-Volume -DriveLetter C | Select-Object -ExpandProperty SizeRemaining) / 1GB", "(Get-Volume -DriveLetter C | Select-Object -ExpandProperty Size) / 1GB"]

#Puis 0-1 pour avoir l'espace utilisé (attention on remet en Go, donc les capacités change par rapport au byte)
```

**Versions** : 
- V1. Base du code 
- V1.2. Ajout de l'agent *network*
- V1.5. Optimisation par dictionnaire
- V1.6. Ajout de l'agent *disk*

**-> Features** : 
- Interface WEB, recherche par ID
- Calcul d'espace dispo -> visulisation par graph WEB

