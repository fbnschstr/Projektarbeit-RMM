'''Bild einlesen und Ordner Dateien erstellen. '''
import csv
import os
import cv2
import imutils as imu
import numpy as np
import pandas as pd
import Functions

def bilder_schneiden(img_folder_path):
    '''------------------------------------------ Programmkonstanten definieren ------------------------------------------'''

    # Bildgröße
    CRP_IMG_WIDTH = 500
    CRP_IMG_HEIGHT  = 500

    # Definieren des Schwellenwerts für Schwarz/Graue Pixel und helle Pixel
    THRESHOLD_EDGE = 255/2
    THRESHOLD_OPENING_POROSITAET = 157
    '''------------------------------------------ Ausgansbilder drehen ------------------------------------------'''
    # Drehe alle png/jpg-Dateien im Unterordner "Bilder" (=img_folder_path)
    for filename in os.listdir(img_folder_path):
        # Überprüfen, ob die Datei eine Bilddatei ist (z. B. .jpg oder .png)
        if not (filename.endswith('.jpg') or filename.endswith('.png')):
            continue

        # Voller Pfad zur Bilddatei
        image_path = os.path.join(img_folder_path, filename)
        
        img = cv2.imread(image_path)
        angle = 180
        Functions.drehen(analysis_path, crp_img_save_path_col, img, angle, filename, False)
    '''------------------------------------------ Bilder zerschneiden ------------------------------------------'''
    for filename in os.listdir(analysis_path):
        # Zerschneide alle (gedrehten) png/jpg-Dateien aus dem Unterordner "Auswertung" (=analysis_path)
        # Überprüfen, ob die Datei eine Bilddatei ist (z. B. .jpg oder .png)
        if not (filename.endswith('.jpg') or filename.endswith('.png')):
            continue

        # Voller Pfad zur Bilddatei
        image_path = os.path.join(analysis_path, filename)
        img = cv2.imread(image_path)

        # Öffne das Bild mit cv2 und konvertiere es in Graustufen
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Anzahl der Bilder aus der Bildgröße bestimmen
        anzahl_bilder_x = img.shape[1] // CRP_IMG_WIDTH
        anzahl_bilder_y = img.shape[0] // CRP_IMG_HEIGHT

        # Rand berechnen der auf beiden Seiten freigehalten werden soll, damit alle Bilder mittig reinpassen
        rand_height = (img.shape[0] % CRP_IMG_HEIGHT) // 2
        rand_width  = (img.shape[1] % CRP_IMG_WIDTH) // 2

        por_list = []
        # Schleife für jeden Zuschneidebereich
        for x in range(anzahl_bilder_x):
            for y in range(anzahl_bilder_y):

                # Berechne die Koordinaten des aktuellen Zuschneidebereichs
                crp_x = (x * int(CRP_IMG_WIDTH)) + rand_width
                crp_y = (y * int(CRP_IMG_HEIGHT) ) + rand_height

                # Dateiname für den zugeschnittenen Bereich
                filename_short = filename[:filename.find('.')]
                crp_img_name = f"{filename_short}_crp_x{x}_y{y}.png"

                # Schneide das Bild entsprechend dem Zuschneidebereich zu
                crp_img = img[crp_y:crp_y + CRP_IMG_HEIGHT, crp_x:crp_x + CRP_IMG_WIDTH]

                if Functions.rand(crp_img, THRESHOLD_EDGE):
                    # Randbild
                    continue

                else: # kein Randbild
                    # Porosität bestimmen
                    por = Functions.getPorositaet(crp_img, THRESHOLD_OPENING_POROSITAET)

                    # Zugeschnittenes Bild drehen und speichern
                    angle = 90
                    rotated_img_list = Functions.drehen(crp_img_save_path, crp_img_save_path_col, crp_img, angle, crp_img_name, True)

                    for rot_img in rotated_img_list:
                        por_class = Functions.get_class(por)
                        por_list.append([rot_img, por, por_class])



        '''Listen in DataFrame zusammenführen und als Excel abspeichern'''
        save_path_xlsx = os.path.join(xlsx_path, "data.xlsx")
        df = pd.DataFrame(data=por_list, columns=['Bildname','Porositaet','Porositeatsklasse'])
        df.to_excel(save_path_xlsx, index=False)
        

if __name__ == '__main__':
    '''------------------------------------------ Ordnerstrucktur aufbauen ------------------------------------------'''
    img_folder_path = Functions.ornder_erstellen("Bilder", os.path.dirname(__file__), delete = False)
    analysis_path = Functions.ornder_erstellen("Auswertung", img_folder_path, delete = False)
    crp_img_save_path = Functions.ornder_erstellen("BW_CRP_Bilder", analysis_path, delete = True)
    crp_img_save_path_col = Functions.ornder_erstellen("COL_CRP_Bilder", analysis_path, delete = True)
    crp_img_save_path_rand = Functions.ornder_erstellen("Rand", analysis_path, delete = True)
    save_path_closing = Functions.ornder_erstellen("Bilder_Closed", analysis_path, delete = True)
    save_path_thhold = Functions.ornder_erstellen("Threshold", save_path_closing, delete = True)
    xlsx_path = Functions.ornder_erstellen("xlsx", analysis_path)
    
    bilder_schneiden(img_folder_path)