'''Bild einlesen und Ordner Dateien erstellen. '''
import os
import cv2
import numpy as np
import pandas as pd     #Notwendig für DataFrame (pip install pandas)

from Porositaetmessung import *
#evtl. muss zusaetzlich 'pip install openpyxl' installiert werden
'''------------------------------------------ ------------------------------------------'''
'''------------------------------------------ Ordnerstrucktur aufbauen ------------------------------------------'''
# Pfad der aktuellen Datei
path = os.path.dirname(__file__)

img_folder_path = os.path.join(path, "Bilder")
print(img_folder_path)
# Erstelle den Ordner für die Bilder, falls noch nicht vorhanden
if not os.path.exists(img_folder_path):
    os.mkdir(img_folder_path)

crp_img_save_path = os.path.join(img_folder_path, "Zugeschnittene_Bilder")
print(crp_img_save_path)
# Erstelle den Ordner für die zugeschnittenen Bilder, falls noch nicht vorhanden
if not os.path.exists(crp_img_save_path):
    os.mkdir(crp_img_save_path)

crp_img_save_path_rand = os.path.join(img_folder_path, "Rand")
print(crp_img_save_path_rand)
# Erstelle den Ordner für die Randbilder, falls noch nicht vorhanden
if not os.path.exists(crp_img_save_path_rand):
    os.mkdir(crp_img_save_path_rand)

save_path_closing = os.path.join(img_folder_path,"Bilder_Closed")
print(save_path_closing)
# Erstelle den Ordner für die Bilder mit "geschlossener Prorsitaetskontur", falls noch nicht vorhanden
if not os.path.exists(save_path_closing):
    os.mkdir(save_path_closing)

save_path_thhold = os.path.join(save_path_closing,"Threshold")
print(save_path_thhold)
# Erstelle den Ordner für die Bilder der Porositaetsmessung, falls noch nicht vorhanden
if not os.path.exists(save_path_thhold):
    os.mkdir(save_path_thhold)

# Pfad zum Abspeichern der Excel-Datei
save_path_xlsx = os.path.join(img_folder_path, "Porositaet.xlsx")

'''------------------------------------------ Programmwerte definieren ------------------------------------------'''
# Länge des Referenzebalkens
referenzbalken_pixel = 1462  # Größe des Referenzbalkens in Pixeln
referenzbalken_mm = 2  # Größe des Referenzbalkens in mm

# Bildgröße
crp_img_width = 500
crp_img_height  = 500

crp_size = True

# Anzahl der Bilder pro Achse bestimmen
anzahl_bilder_x = 12
anzahl_bilder_y = 12

anzahl = False

# Definieren des Schwellenwerts für Schwarz/Graue Pixel und helle Pixel
threshold_edge = 255/2

'''------------------------------------------ Bilder zuschneiden und nach Rand und nicht Randbildern sortieren ------------------------------------------'''

''' Bilder laden und Größe bestimmen'''
# Durchsuche den Ordner nach Dateien
for filename in os.listdir(img_folder_path):
    # Überprüfen, ob die Datei eine Bilddatei ist (z. B. .jpg oder .png)
    if not (filename.endswith('.jpg') or filename.endswith('.png')):
        continue

    # Voller Pfad zur Bilddatei
    image_path = os.path.join(img_folder_path, filename)
    file_name = f"{filename}"
    #print("Name:",file_name)
    
    # Öffne das Bild mit cv2 und konvertiere es in Graustufen
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Bestimme die Größe des Bildes in mm (Annahme: Größe des Referenzbalkens ist bekannt)
    # Beispielhaft wird hier die Größe als (Breite, Höhe) in mm ausgegeben
    breite_mm = img.shape[1] * referenzbalken_mm / referenzbalken_pixel
    höhe_mm = img.shape[0] * referenzbalken_mm / referenzbalken_pixel
    
    # Ausgabe der Bildgröße
    print(f"Datei: {filename} | Breite: {breite_mm} mm | Höhe: {höhe_mm} mm")

    #crp_breite = crp_img_width
    #crp_hoehe  = crp_img_height

    # Anzahl der Bilder aus der Bildgröße bestimmen
    anzahl_bilder_x = img.shape[1] // crp_img_width
    anzahl_bilder_y = img.shape[0] // crp_img_height

    # Rand berechnen der auf beiden Seiten freigehalten werden soll, damit alle Bilder mittig reinpassen
    rand_height = (img.shape[0] % crp_img_height) // 2
    rand_width  = (img.shape[1] % crp_img_width) // 2

    # Initialisierung der leeren Listen für für Porosität und Bildnamen (notwendig um Excel zu generieren)
    i = 0       # Durchlaufvariable der Listeneinträge
    porositaet_list = []
    name_list = []

    ''' Bilder zuschneiden '''
    # Schleife für jeden Zuschneidebereich
    for x in range(anzahl_bilder_x):
        for y in range(anzahl_bilder_y):
            
            # Berechne die Koordinaten des aktuellen Zuschneidebereichs
            crp_x = (x * int(crp_img_width)) + rand_width
            crp_y = (y * int(crp_img_height) ) + rand_height
            
            # Dateiname für den zugeschnittenen Bereich
            # Zuvor wird die Dateiendung (alles hinter dem letzten Punkt) im Dateinamen abgeschnitten --> hier wird dann die weitere Dateibezeichnung angehängt
            file_name_short = file_name[:file_name.find('.')]
            crp_name = f"{file_name_short}_crp_x_{x}_y_{y}.png"  

            # Schneide das Bild entsprechend dem Zuschneidebereich zu
            crp_img = img[crp_y:crp_y + crp_img_height, crp_x:crp_x + crp_img_width]

            # Mittelwerte der Außenkanten berechnen
            mean_top = np.mean(crp_img[0, :])
            mean_bottom = np.mean(crp_img[crp_img_height - 1 , :])
            mean_right = np.mean(crp_img[:, crp_img_width - 1])
            mean_left = np.mean(crp_img[:,0])

            if mean_top < threshold_edge or mean_bottom < threshold_edge or mean_right < threshold_edge or mean_left < threshold_edge:     
                # Speichere den zugeschnittenen Bereich ab, falls der Mittelwert größer als der Threshold ist
                # Randbild
                img_crp_save_path = os.path.join(crp_img_save_path_rand,crp_name)
                #os.mkdir(img_crp_save_path + filename)
                # Speichere das zugeschnittene Bild
                cv2.imwrite(img_crp_save_path, crp_img)
            else:
                # Speichere den zugeschnittenen Bereich ab, falls der Mittelwert kleiner oder gleich dem Threshold ist
                # kein Randbild
                img_crp_save_path1 = os.path.join(crp_img_save_path,crp_name)
                
                # Speichere das zugeschnittene Bild
                cv2.imwrite(img_crp_save_path1, crp_img)

                #Porositaet aufrufen und bestimmen (Prorsitaetswert in Variabler dummy zwischen speichern, anschließend Listen generieren)
                ##getPorositaet(crp_img_save_path, save_path_closing, save_path_thhold, crp_name)
                i = i+1     #Durchlaufvariable zum kontinuirlichen Beschreiben der Listen-Variablen (porositaet.list und name_list)
                dummy = getPorositaet(crp_img_save_path, save_path_closing, save_path_thhold, crp_name)
                porositaet_list.insert(i, dummy)
                name_list.insert(i, crp_name)

'''Listen in DataFrame zusammenführen und als Excel abspeichern'''
df = pd.DataFrame(data=zip(name_list, porositaet_list), columns=['Bildname','Porositaet'])
#print(df)
df.to_excel(save_path_xlsx, index=False)
