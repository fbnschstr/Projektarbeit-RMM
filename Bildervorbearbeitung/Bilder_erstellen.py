'''Bild einlesen und Ordner Dateien erstellen. '''
import csv
import os
import cv2
import numpy as np
import pandas as pd
import Porositaetmessung
'''------------------------------------------ ------------------------------------------'''
def ornder_erstellen(ordner_name, ordner_pfad, delete = False):
    pfad_ersteller_ordner = os.path.join(ordner_pfad, ordner_name)
    if os.path.exists(pfad_ersteller_ordner):
        if delete:
            #for f in os.listdir(pfad_ersteller_ordner):
            #    os.remove(os.path.join(pfad_ersteller_ordner, f))
            print("muss noch gemacht werden")
        return pfad_ersteller_ordner
    os.mkdir(pfad_ersteller_ordner)
    return pfad_ersteller_ordner
'''------------------------------------------ ------------------------------------------'''
def rand(img, threshold, bilder_x, bilder_y):
    x, y = bilder_x, bilder_y
    height, width = img.shape

    mean_values = [np.mean(img[0, :]), np.mean(img[height-1, :]), np.mean(img[:, 0]), np.mean(img[:, width-1])]

    comparison = any(mean_values) > threshold or x in [0, bilder_x-1] or y in [0, bilder_y-1]

    if comparison:
        return True
    return False
'''------------------------------------------ Ordnerstrucktur aufbauen ------------------------------------------'''
# Pfad der aktuellen Datei
path = os.path.dirname(__file__)

img_folder_path = ornder_erstellen("Bilder", path, delete = False)
crp_img_save_path = ornder_erstellen("Zugeschnittene_Bilder", img_folder_path, delete = True)
crp_img_save_path_rand = ornder_erstellen("Rand", img_folder_path, delete = True)
save_path_closing = ornder_erstellen("Bilder_Closed", img_folder_path, delete = True)
save_path_thhold = ornder_erstellen("Threshold", save_path_closing, delete = True)
#save_path_xlsx = os.path.join(img_folder_path, "Porositaet.xlsx")


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
    save_path_xlsx = os.path.join(img_folder_path, "Porositaet" + filename[:filename.find('.')] + ".xlsx")
    if not (filename.endswith('.jpg') or filename.endswith('.png')):
        continue

    # Voller Pfad zur Bilddatei
    image_path = os.path.join(img_folder_path, filename)
    
    # Öffne das Bild mit cv2 und konvertiere es in Graustufen
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Bestimme die Größe des Bildes in mm (Annahme: Größe des Referenzbalkens ist bekannt)
    # Beispielhaft wird hier die Größe als (Breite, Höhe) in mm ausgegeben
    breite_mm = img.shape[1] * REFERENZBALKEN_MM / REFERENZBALKEN_PIXEL
    höhe_mm = img.shape[0] * REFERENZBALKEN_MM / REFERENZBALKEN_PIXEL
    
    # Ausgabe der Bildgröße
    print(f"Datei: {filename} | Breite: {breite_mm} mm | Höhe: {höhe_mm} mm")

    #crp_breite = CRP_IMG_WIDTH
    #crp_hoehe  = CRP_IMG_HEIGHT

    # Anzahl der Bilder aus der Bildgröße bestimmen
    anzahl_bilder_x = img.shape[1] // CRP_IMG_WIDTH
    anzahl_bilder_y = img.shape[0] // CRP_IMG_HEIGHT

    # Rand berechnen der auf beiden Seiten freigehalten werden soll, damit alle Bilder mittig reinpassen
    rand_height = (img.shape[0] % CRP_IMG_HEIGHT) // 2
    rand_width  = (img.shape[1] % CRP_IMG_WIDTH) // 2

    # Initialisierung der leeren Listen für für Porosität und Bildnamen (notwendig um Excel zu generieren)
    i = 0       # Durchlaufvariable der Listeneinträge
    porositaet_list = []
    name_list = []

    ''' Bilder zuschneiden '''
    # Schleife für jeden Zuschneidebereich
    for x in range(anzahl_bilder_x):
        for y in range(anzahl_bilder_y):
            
            # Berechne die Koordinaten des aktuellen Zuschneidebereichs
            crp_x = (x * int(CRP_IMG_WIDTH)) + rand_width
            crp_y = (y * int(CRP_IMG_HEIGHT) ) + rand_height
            
            # Dateiname für den zugeschnittenen Bereich
            # Zuvor wird die Dateiendung (alles hinter dem letzten Punkt) im Dateinamen abgeschnitten --> hier wird dann die weitere Dateibezeichnung angehängt
            filename_short = filename[:filename.find('.')]
            crp_name = f"{filename_short}_crp_x_{x}_y_{y}.png"  

            # Schneide das Bild entsprechend dem Zuschneidebereich zu
            crp_img = img[crp_y:crp_y + CRP_IMG_HEIGHT, crp_x:crp_x + CRP_IMG_WIDTH]

            # if mean_top < THRESHOLD_EDGE or mean_bottom < THRESHOLD_EDGE or mean_right < THRESHOLD_EDGE or mean_left < THRESHOLD_EDGE:
            if x == 0 or y == 0 or x == anzahl_bilder_x -1 or y == anzahl_bilder_y -1 or rand(crp_img,THRESHOLD_EDGE,anzahl_bilder_x,anzahl_bilder_y):
                # Speichere den zugeschnittenen Bereich ab, falls der Mittelwert größer als der Threshold ist
                # Randbild
                img_crp_save_path = os.path.join(crp_img_save_path_rand,crp_name)
                #os.mkdir(img_crp_save_path + filename)
                # Speichere das zugeschnittene Bild
                cv2.imwrite(img_crp_save_path, crp_img)
            else:
                # Speichere den zugeschnittenen Bereich ab, falls der Mittelwert kleiner oder gleich dem Threshold ist
                # kein Randbild
                img_crp_save_path = os.path.join(crp_img_save_path,crp_name)
                
                # Speichere das zugeschnittene Bild
                cv2.imwrite(img_crp_save_path, crp_img)

                #Porositaet aufrufen und bestimmen (Prorsitaetswert in Variabler dummy zwischen speichern, anschließend Listen generieren)
                i = i+1     #Durchlaufvariable zum kontinuirlichen Beschreiben der Listen-Variablen (porositaet.list und name_list)
                porositeat = Porositaetmessung.getPorositaet(crp_img_save_path, save_path_closing, save_path_thhold, crp_name)
                porositaet_list.insert(i, porositeat)
                name_list.insert(i, crp_name)

    '''Listen in DataFrame zusammenführen und als Excel abspeichern'''
    df = pd.DataFrame(data=zip(name_list, porositaet_list), columns=['Bildname','Porositaet'])
    #print(df)
    df.to_excel(save_path_xlsx, index=False)