'''Bild einlesen und Ordner Dateien erstellen. '''
import csv
import os
import cv2
import imutils as imu
import numpy as np
import pandas as pd
import Porositaetmessung
import matplotlib.pyplot as plt
'''------------------------------------------ Exeptions ---------------------------------------'''
class MultipleCirclesError(Exception):
    def __init__(self, message="Mehr als ein Kreis wurde erkannt."):
        self.message = message
        super().__init__(self.message)

class NoCircleDetectedError(Exception):
    def __init__(self, message="Kein Kreis wurde erkannt."):
        self.message = message
        super().__init__(self.message)


'''------------------------------------------ Ordner erstellen ---------------------------------------'''
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
'''------------------------------------------ Rand erkennen ------------------------------------------'''
def rand_erkennen(img, threshold):
    height, width = img.shape
    black_row = False
    black_column = False
    radius = kreis_erkennen2(img)

    for row in range(height):
        if np.mean(img[row,:]) < threshold:
            black_row = True

    for column in range(width):
        if np.mean(img[:,column]) < threshold:
            black_column = True

    if black_column or black_row:
        return True
    return False

def rand_erkennen2(img, threshold, org_image, circle_center, image_position):
    height, width = img.shape

    for row in range(height):
        if np.mean(img[row, :]) < threshold:
            return True

    for column in range(width):
        if np.mean(img[:, column]) < threshold:
            return True

    # Überprüfen, ob das Bild img auf dem erkannten Kreis im Originalbild liegt
    center_x, center_y, radius = circle_center[0]
    img_x, img_y = image_position

    # Berechnen Sie die tatsächlichen Koordinaten des Bildes img im Originalbild
    img_x_in_org = img_x + center_x
    img_y_in_org = img_y + center_y

    # Überprüfen, ob der Umfang des Kreises im Bereich des Bildes liegt
    if(
        (center_x - radius > img_x + 500) or
        (center_x + radius < img_x) or
        (center_y - radius > img_y + 500) or
        (center_y + radius < img_y)
    ): 
        return True

    return False
'''------------------------------------------ Bilder drehen ------------------------------------------'''
def drehen(filename, image_save_path, image, angle):
    
    number_rotations = 360 // angle
    rot_img_save_path = ornder_erstellen("gedrehte Bilder", image_save_path, delete= True)
    
    for x in range(number_rotations):
        cal_angle = angle + x * angle
        # Cal steht für calculated
        rotated_img = imu.rotate_bound(image, cal_angle)
        # Um nur den ersten Teil des getrennten Namens zu speichern
        filename_short = os.path.splitext(filename)[0]
        rotated_name = f"{filename_short}_Winkel_{cal_angle}.png"
        save_path = os.path.join(rot_img_save_path, rotated_name)
        cv2.imwrite(save_path, rotated_img)
    return rot_img_save_path

""" def kreis_erkennen(org_image):
    # Initialisiere den SimpleBlobDetector mit benutzerdefinierten Parametern
    params = cv2.SimpleBlobDetector_Params()
    # Filtere nach Kreisen, die helle Bereiche auf dunklem Hintergrund darstellen
    params.filterByColor = True
    params.blobColor = 255
    # Filtere nach Kreisen die mind. eine Fläche von minArea umschließen
    # Setze die Mindest- und Höchstdurchmesser der Kreise (Radius * 2)
    params.filterByArea = True
    min_diameter = 2000  # Mindestdurchmesser
    max_diameter = 10000  # Maximaldurchmesser
    params.minArea = np.pi * (min_diameter / 2) ** 2  # Mindestfläche basierend auf dem Mindestdurchmesser
    params.maxArea = np.pi * (max_diameter / 2) ** 2  # Maximale Fläche basierend auf dem Maximaldurchmesser

    detector = cv2.SimpleBlobDetector_create(params)
    path = "Bildervorbearbeitung/Bilder"
    path = os.path.dirname(org_image)

    for image in os.listdir(path):
        if not image.endswith('rund.png'):
            continue
        image_path = os.path.join(path, image)
        image = cv2.imread(image_path)
        # Konvertiere das Bild in Graustufen
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Erkenne die Kreise im Bild
        keypoints = detector.detect(gray)

        # Extrahiere die Koordinaten und Radien der erkannten Kreise
        circles = []
        for keypoint in keypoints:
            x = int(keypoint.pt[0])  # x-Koordinate des Kreises
            y = int(keypoint.pt[1])  # y-Koordinate des Kreises
            radius = int(keypoint.size / 2)  # Radius des Kreises
            circles.append((x, y, radius))
        
        # # Zeige das Bild mit Matplotlib und den erkannten Kreisen
        # plt.figure(figsize=(8, 8))
        # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # for circle in circles:
        #     x, y, radius = circle
        #     circle_obj = plt.Circle((x, y), radius, color='green', fill=False, linewidth=2)
        #     plt.gca().add_patch(circle_obj)
        # plt.axis('off')
        # plt.show()
        return radius
 """
def kreis_erkennen2(image):
    # Initialisiere den SimpleBlobDetector mit benutzerdefinierten Parametern
    params = cv2.SimpleBlobDetector_Params()

    # Filtere nach Kreisen, die helle Bereiche auf dunklem Hintergrund darstellen
    params.filterByColor = True
    params.blobColor = 255

    # Filtere nach Kreisen, die mindestens eine Fläche von minArea umschließen
    # Setze die Mindest- und Höchstdurchmesser der Kreise (Radius * 2)
    params.filterByArea = True
    min_diameter = 2000  # Mindestdurchmesser
    max_diameter = 10000  # Maximaldurchmesser
    params.minArea = np.pi * (min_diameter / 2) ** 2  # Mindestfläche basierend auf dem Mindestdurchmesser
    params.maxArea = np.pi * (max_diameter / 2) ** 2  # Maximale Fläche basierend auf dem Maximaldurchmesser

    detector = cv2.SimpleBlobDetector_create(params)

    # Konvertiere das Bild in Graustufen
    '''wurde schon in Bilder schneiden gemacht'''
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Erkenne die Kreise im Bild
    keypoints = detector.detect(image)

    # Extrahiere die Koordinaten und Radien der erkannten Kreise
    circles = []
    if len(keypoints) == 0:
        raise NoCircleDetectedError()
    
    else:
        for keypoint in keypoints:
            x = int(keypoint.pt[0])  # x-Koordinate des Kreises
            y = int(keypoint.pt[1])  # y-Koordinate des Kreises
            radius = int(keypoint.size / 2)  # Radius des Kreises
            circles.append((x, y, radius))

    # Gibt die Liste der erkannten Kreise (x, y, Radius) zurück
    return circles

def bilder_schneiden(img_folder_path):
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
    THRESHOLD_EDGE = 255 / 2
    THRESHOLD_OPENING_POROSITAET = 157

    for filename in os.listdir(img_folder_path):
        
        save_path_xlsx = os.path.join(xlsx_path, "Porositaet_" + filename[:filename.find('.')] + ".xlsx")
        # Überprüfen, ob die Datei eine Bilddatei ist (z. B. .jpg oder .png)
        if not (filename.endswith('.jpg') or filename.endswith('.png')):
            continue

        # Voller Pfad zur Bilddatei
        image_path = os.path.join(img_folder_path, filename)
        
        '''------------------------------------------ Bilder einlesen und drehen ------------------------------------------'''
        # Öffne das Bild
        img = cv2.imread(image_path)

        # Konvertiere es in Graustufen
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Kreis erkennen
        detected_circles = kreis_erkennen2(img)

        # Überprüfe, ob nur ein Kreis erkannt wurde
        if len(detected_circles) == 1:
        # Nur ein Kreis wurde erkannt
            x, y, radius = detected_circles[0]
        else:
            raise MultipleCirclesError() 
        
        # Bestimme die Größe des Bildes in mm (Annahme: Größe des Referenzbalkens ist bekannt)
        breite_mm = img.shape[1] * REFERENZBALKEN_MM / REFERENZBALKEN_PIXEL
        höhe_mm = img.shape[0] * REFERENZBALKEN_MM / REFERENZBALKEN_PIXEL
        
        # Ausgabe der Bildgröße
        # print(f"Datei: {filename} | Breite: {breite_mm} mm | Höhe: {höhe_mm} mm")

        # Anzahl der Bilder aus der Bildgröße bestimmen
        anzahl_bilder_x = img.shape[1] // CRP_IMG_WIDTH
        anzahl_bilder_y = img.shape[0] // CRP_IMG_HEIGHT

        # Rand berechnen der auf beiden Seiten freigehalten werden soll, damit alle Bilder mittig reinpassen
        rand_height = (img.shape[0] % CRP_IMG_HEIGHT) // 2
        rand_width  = (img.shape[1] % CRP_IMG_WIDTH) // 2

        # Initialisierung der leeren Listen für für Porosität und Bildnamen (notwendig um Excel zu generieren)
        listeneinstrag = 0
        porositaet_list = []
        name_list = []

        '''------------------------------------------ Bilder zerschneiden und aussortieren ------------------------------------------'''
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

                # Schneide das Bild entsprechend dem Zuschneidebereich zu
                crp_img = img[crp_y:crp_y + CRP_IMG_HEIGHT, crp_x:crp_x + CRP_IMG_WIDTH]

                if rand_erkennen2(img= crp_img, threshold= THRESHOLD_EDGE, org_image= img, circle_center= detected_circles, image_position= (crp_x, crp_y) ):
                    # Randbild
                    img_crp_save_path = os.path.join(crp_img_save_path_rand,crp_name)
                    # Speichere das zugeschnittene Bild
                    cv2.imwrite(img_crp_save_path, crp_img)
                else:
                    # kein Randbild
                    img_crp_save_path = os.path.join(crp_img_save_path,crp_name)

                    # Speichere das zugeschnittene Bild
                    cv2.imwrite(img_crp_save_path, crp_img)

                    # Porositaet aufrufen und bestimmen (Prorsitaetswert in Variabler dummy zwischen speichern, anschließend Listen generieren)
                    # Durchlaufvariable zum kontinuirlichen Beschreiben der Listen-Variablen (porositaet.list und name_list)
                    listeneinstrag = listeneinstrag + 1
                    porositeat = Porositaetmessung.getPorositaet(crp_img_save_path, save_path_closing, save_path_thhold, crp_name, THRESHOLD_OPENING_POROSITAET)
                    porositaet_list.insert(listeneinstrag, porositeat)
                    name_list.insert(listeneinstrag, crp_name)

        # Listen in DataFrame zusammenführen und als Excel abspeichern
        df = pd.DataFrame(data=zip(name_list, porositaet_list), columns=['Bildname','Porositaet'])
        df.to_excel(save_path_xlsx, index=False)

if __name__ == '__main__':
    img_folder_path = ornder_erstellen("Bilder", os.path.dirname(__file__), delete = False)

    '''------------------------------------------ Originalbilder drehen ------------------------------------------'''
    """     # Alle vorhandenen Bilder drehen und im richtigem Ordner abspeichern
    for filename in os.listdir(img_folder_path):
        if not (filename.endswith('.jpg') or filename.endswith('.png')):
            continue
        # Voller Pfad zur Bilddatei
        image_path = os.path.join(img_folder_path, filename)
        img = cv2.imread(image_path)

        rotated_image_path = drehen(filename= filename, image_save_path= img_folder_path, image= img, angle= 90)
    """
    '''------------------------------------------ Ordnerstrucktur aufbauen ------------------------------------------'''
    crp_img_save_path = ornder_erstellen("Zugeschnittene_Bilder", img_folder_path, delete = True)
    crp_img_save_path_rand = ornder_erstellen("Rand", img_folder_path, delete = True)
    save_path_closing = ornder_erstellen("Bilder_Closed", img_folder_path, delete = True)
    save_path_thhold = ornder_erstellen("Threshold", save_path_closing, delete = True)
    xlsx_path = ornder_erstellen("xlsx", img_folder_path)

    '''------------------------------------------ Originalbidler zerschneiden ------------------------------------------'''
    # Die gedrehten Originalbilder werden geschnitten
    # Um die grdrehten Originalbilder zu zerschniden img_folder_path in rotated_image_path ändern
    for filename in os.listdir(img_folder_path):
        bilder_schneiden(img_folder_path)

    '''------------------------------------------ Datensatz vergrößern ------------------------------------------'''
    # Um den Datensatz zu vergrößern, werden die kleinen 500 x 500 Bilder 4 mal um 90 Grad gedreht
    for filename in os.listdir(rotated_image_path):
        if not (filename.endswith('.jpg') or filename.endswith('.png')):
            continue
        # Voller Pfad zur Bilddatei
        image_path = os.path.join(rotated_image_path, filename)
        img = cv2.imread(image_path)

        rotated_image_path = drehen(filename= filename, image_save_path= crp_img_save_path, image= img, angle= 90)
