'''Bild einlesen und Ordner Dateien erstellen. '''
import csv
import os
import cv2
import imutils as imu
import numpy as np
import pandas as pd
import Functions

def bilder_schneiden(img_folder_path)
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
    THRESHOLD_OPENING_POROSITAET = 157

    # Drehe alle png/jpg-Dateien im Unterordner "Bilder" (=img_folder_path)
    for filename in os.listdir(img_folder_path):
        # Überprüfen, ob die Datei eine Bilddatei ist (z. B. .jpg oder .png)
        save_path_xlsx = os.path.join(xlsx_path, "Porositaet_" + filename[:filename.find('.')] + ".xlsx")
        if not (filename.endswith('.jpg') or filename.endswith('.png')):
            continue

        # Voller Pfad zur Bilddatei
        image_path = os.path.join(img_folder_path, filename)
        
        '''------------------------------------------ Bilder drehen ------------------------------------------'''
        img = cv2.imread(image_path)
        angle = 180
        Functions.drehen(analysis_path, img, angle, filename)

    # Zerschneide alle (gedrehten) png/jpg-Dateien aus dem Unterordner "Auswertung" (=analysis_path)
    for filename in os.listdir(analysis_path): 
        # Überprüfen, ob die Datei eine Bilddatei ist (z. B. .jpg oder .png)
        save_path_xlsx = os.path.join(xlsx_path, "Porositaet_" + filename[:filename.find('.')] + ".xlsx")
        if not (filename.endswith('.jpg') or filename.endswith('.png')):
            continue

        # Voller Pfad zur Bilddatei
        image_path = os.path.join(analysis_path, filename)
        img = cv2.imread(image_path)
        '''------------------------------------------ Bilder in Schwarz-Weiß konvertieren ------------------------------------------'''
        
        # Öffne das Bild mit cv2 und konvertiere es in Graustufen
        #img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Bestimme die Größe des Bildes in mm (Annahme: Größe des Referenzbalkens ist bekannt)
        # Beispielhaft wird hier die Größe als (Breite, Höhe) in mm ausgegeben
        breite_mm = img.shape[1] * REFERENZBALKEN_MM / REFERENZBALKEN_PIXEL
        höhe_mm = img.shape[0] * REFERENZBALKEN_MM / REFERENZBALKEN_PIXEL

        # Ausgabe der Bildgröße
        print(f"Datei: {filename} | Breite: {breite_mm} mm | Höhe: {höhe_mm} mm")

        # Anzahl der Bilder aus der Bildgröße bestimmen
        anzahl_bilder_x = img.shape[1] // CRP_IMG_WIDTH
        anzahl_bilder_y = img.shape[0] // CRP_IMG_HEIGHT

        # Rand berechnen der auf beiden Seiten freigehalten werden soll, damit alle Bilder mittig reinpassen
        rand_height = (img.shape[0] % CRP_IMG_HEIGHT) // 2
        rand_width  = (img.shape[1] % CRP_IMG_WIDTH) // 2

        # Initialisierung der leeren Listen für für Porosität und Bildnamen (notwendig um Excel zu generieren)
        # listeneinstrag = 0
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
                crp_name = f"{filename_short}_crp_x{x}_y{y}.png"
                #crp_name = f"{filename}_crp_x{x}_y{y}.png"

                # Schneide das Bild entsprechend dem Zuschneidebereich zu
                crp_img = img[crp_y:crp_y + CRP_IMG_HEIGHT, crp_x:crp_x + CRP_IMG_WIDTH]

                if Functions.rand(crp_img, THRESHOLD_EDGE):
                    # Randbild
                    img_crp_save_path = os.path.join(crp_img_save_path_rand,crp_name)
                    # Speichere das zugeschnittene Bild
                    cv2.imwrite(img_crp_save_path, crp_img)
                else:
                    # kein Randbild
                    img_crp_save_path_rotate = crp_img_save_path
                    img_crp_save_path = os.path.join(crp_img_save_path,crp_name)

                    # Zugeschnittenes Bild drehen
                    angle = 90
                    Functions.drehen(img_crp_save_path_rotate, crp_img, angle, crp_name)

                    # # Speichere das zugeschnittene Bild
                    # cv2.imwrite(img_crp_save_path, crp_img)

    for filename_cropped_rotated, listeneinstrag in zip(os.listdir(img_crp_save_path_rotate), range(1, len(os.listdir(img_crp_save_path_rotate))+1)):
        # Porositaet aufrufen und bestimmen (Prorsitaetswert in Variabler dummy zwischen speichern, anschließend Listen generieren)
        # listeneinstrag = listeneinstrag + 1     #Durchlaufvariable zum kontinuirlichen Beschreiben der Listen-Variablen (porositaet.list und name_list)
        porositeat = Functions.getPorositaet(img_crp_save_path_rotate, save_path_closing, save_path_thhold, filename_cropped_rotated, THRESHOLD_OPENING_POROSITAET)
        porositaet_list.insert(listeneinstrag, porositeat)
        name_list.insert(listeneinstrag, filename_cropped_rotated)

    '''Listen in DataFrame zusammenführen und als Excel abspeichern'''
    df = pd.DataFrame(data=zip(name_list, porositaet_list), columns=['Bildname','Porositaet'])
    df.to_excel(save_path_xlsx, index=False)



if __name__ == '__main__':
    img_folder_path = Functions.ornder_erstellen("Bilder", os.path.dirname(__file__), delete = False)

    '''------------------------------------------ Ordnerstrucktur aufbauen ------------------------------------------'''
    analysis_path = Functions.ornder_erstellen("Auswertung", img_folder_path, delete = False)

    crp_img_save_path = Functions.ornder_erstellen("Zugeschnittene_Bilder", analysis_path, delete = True)
    crp_img_save_path_rand = Functions.ornder_erstellen("Rand", analysis_path, delete = True)
    save_path_closing = Functions.ornder_erstellen("Bilder_Closed", analysis_path, delete = True)
    save_path_thhold = Functions.ornder_erstellen("Threshold", save_path_closing, delete = True)
    xlsx_path = Functions.ornder_erstellen("xlsx", analysis_path)
    
    bilder_schneiden(img_folder_path)
