'''Bild einlesen und Ordner Dateien erstellen. '''
import csv
import os
import cv2
import numpy as np
#import Poroesitaetmessung
'''------------------------------------------ ------------------------------------------'''
def struktur_erstellen(name_pfad, ort_pfad):
    name_pfad = os.path.join(os.path.dirname(ort_pfad), name_pfad)
    if not os.path.exists(name_pfad):
        os.mkdir(name_pfad)
    return name_pfad

'''------------------------------------------ Ordnerstrucktur aufbauen ------------------------------------------'''
# Pfad der aktuellen Datei
path = os.path.dirname(__file__)

img_folder_path = struktur_erstellen("Bilder", path)
crp_img_save_path = struktur_erstellen("Zugeschnittene_Bilder", path)
crp_img_save_path_rand = struktur_erstellen("Rand", path)
csv_path = struktur_erstellen("csv", path)

'''------------------------------------------ Programmkonstanten definieren ------------------------------------------'''
#Länge des Referenzebalkens
REFERENZBALKEN_PIXEL = 1462  # Größe des Referenzbalkens in Pixeln
REFERENZBALKEN_MM = 2  # Größe des Referenzbalkens in mm

# Bildgröße
CRP_IMG_WIDTH = 500
CRP_IMG_HEIGHT  = 500

# Anzahl der Biilder pro Achse bestimmen bestimmen
ANZAHL_BILDER_X = 12
ANZAHL_BILDER_Y = 12

# Definieren des Schwellenwerts für Schwarz/Graue Pixel und helle Pixel
THRESHOLD_EDGE = 255/2
'''------------------------------------------ Bilder zuschneiden und nach Rand und nicht Randbildern sortieren ------------------------------------------'''

''' Bilder laden und Größe bestimmen'''
# Durchsuche den Ordner nach Dateien
for filename in os.listdir(img_folder_path):
    # Überprüfen, ob die Datei eine Bilddatei ist (z. B. .jpg oder .png)
    if not (filename.endswith('.jpg') or filename.endswith('.png')):
        continue

    # Voller Pfad zur Bilddatei
    image_path = os.path.join(img_folder_path, filename)
    # Erstelle .csv Datei
    csv_name = "csv_" + filename[:-4] + ".csv"
    os.chdir(csv_path)
    if os.path.exists(csv_name):
        os.remove(csv_name)
    with open(csv_name, 'x', newline='') as csv_file:
        csvwriter = csv.writer(csv_file)
        csvwriter.writerow(['x', 'y', 'Porosität'])

    # Öffne das Bild mit cv2 und konvertiere es in Graustufen
    img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
    
    # Bestimme die Größe des Bildes in mm (Annahme: Größe des Referenzbalkens ist bekannt)
    # Beispielhaft wird hier die Größe als (Breite, Höhe) in mm ausgegeben
    breite_mm = img.shape[1] * REFERENZBALKEN_MM / REFERENZBALKEN_PIXEL
    höhe_mm = img.shape[0] * REFERENZBALKEN_MM / REFERENZBALKEN_PIXEL
    
    # Ausgabe der Bildgröße
    #print(f"Datei: {filename} | Breite: {breite_mm} mm | Höhe: {höhe_mm} mm")

    # Anzahl der Bilder aus der Bildgröße bestimmen
    ANZAHL_BILDER_X = img.shape[1] // CRP_IMG_WIDTH
    ANZAHL_BILDER_Y = img.shape[0] // CRP_IMG_HEIGHT

    # Rand berechnen der auf beiden Seiten freigehalten werden soll, damit alle Bilder mittig reinpassen
    rand_height = (img.shape[0] % CRP_IMG_HEIGHT) // 2
    rand_width  = (img.shape[1] % CRP_IMG_WIDTH) // 2

    ''' Bilder zuschneiden '''
    # Schleife für jeden Zuschneidebereich
    for x in range(ANZAHL_BILDER_X):
        for y in range(ANZAHL_BILDER_Y):
            
            # Berechne die Koordinaten des aktuellen Zuschneidebereichs
            crp_x = (x * int(CRP_IMG_WIDTH)) + rand_width
            crp_y = (y * int(CRP_IMG_HEIGHT) ) + rand_height
            
            # Dateiname für den zugeschnittenen Bereich
            crp_name = f"{filename[:-4]}_crp_x_{x}_y_{y}.png" 

            # Schneide das Bild entsprechend dem Zuschneidebereich zu
            crp_img = img[crp_y:crp_y + CRP_IMG_HEIGHT, crp_x:crp_x + CRP_IMG_WIDTH]

            # Mittelwerte der Außenkanten berechnen
            mean_top = np.mean(crp_img[0, :])
            mean_bottom = np.mean(crp_img[CRP_IMG_HEIGHT - 1 , :])
            mean_right = np.mean(crp_img[:, CRP_IMG_WIDTH - 1])
            mean_left = np.mean(crp_img[:,0])
            
            if mean_top < THRESHOLD_EDGE or mean_bottom < THRESHOLD_EDGE or mean_right < THRESHOLD_EDGE or mean_left < THRESHOLD_EDGE:     
                # Randbild
                continue
            cv2.imwrite(crp_img_save_path + crp_name, crp_img)
                # CSV-Datei schreiben
            with open(csv_name, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                # Schreibe Überschriften, falls die Datei neu ist
                # Schreibe Werte
                csvwriter.writerow([crp_name, x, y, 1])