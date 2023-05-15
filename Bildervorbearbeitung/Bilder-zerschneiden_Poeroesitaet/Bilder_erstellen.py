'''Bild einlesen und Ordner Dateien erstellen. '''
import os
import cv2
import numpy as np

# Pfad anlegen, automatiesiert, in dem Ordner, wo man sich gerade befindet 
# Der Befehl os.getcwd() gibt dabei den Order aus, in dem das Programm geladen ist. Bei Bedarf muss nur path = geändert werden. Die restlichen Pfade werden automatisch angepasst.
path = os.getcwd()

img_folder_path = os.getcwd()
print(img_folder_path)

crp_img_save_path = os.path.join(img_folder_path, "Zugeschnittene_Bilder")
print(crp_img_save_path)

crp_img_save_path_rand = os.path.join(img_folder_path, "Rand")
print(crp_img_save_path_rand)

# Erstelle den Ordner für die zugeschnittenen Bilder, falls noch nicht vorhanden
if not os.path.exists(crp_img_save_path):
    os.mkdir(crp_img_save_path)
    print(f'Ordner "{crp_img_save_path}" wurde erstellt.')
else:
    print(f'Ordner "{crp_img_save_path}" ist vorhanden.')

# Erstelle den Ordner für die  Bilder, falls noch nicht vorhanden
if not os.path.exists(img_folder_path):
    os.mkdir(img_folder_path)
    print(f'Ordner "{img_folder_path}" wurde erstellt.')
else:
    print(f'Ordner "{img_folder_path}" ist vorhanden.')

# Erstelle den Ordner für die Randbilder, falls noch nicht vorhanden
if not os.path.exists(crp_img_save_path_rand):
    os.mkdir(crp_img_save_path_rand)
    print(f'Ordner "{crp_img_save_path_rand}" wurde erstellt.')
else:
    print(f'Ordner "{crp_img_save_path_rand}" ist vorhanden.')
#Länge des Referenzebalkens
referenzbalken_pixel = 1462  # Größe des Referenzbalkens in Pixeln
referenzbalken_mm = 2  # Größe des Referenzbalkens in mm

# Bildgröße
crp_img_width = 500
crp_img_height  = 500

crp_size = True

# Anzahl der Biilder pro Achse bestimmen bestimmen
anzahl_bilder_x = 12
anzahl_bilder_y = 12

anzahl = False

# Definieren des Schwellenwerts für Schwarz/Graue Pixel und helle Pixel
threshold_edge = 255/2


''' Bilder laden und Größe bestimmen'''


# Durchsuche den Ordner nach Dateien

for filename in os.listdir(img_folder_path):
    # Überprüfen, ob die Datei eine Bilddatei ist (z. B. .jpg oder .png)
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Voller Pfad zur Bilddatei
        image_path = os.path.join(img_folder_path, filename)
        file_name = f"{filename}"
        print("Name:",file_name)
        
        # Öffne das Bild mit cv2 und konvertiere es in Graustufen
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Bestimme die Größe des Bildes in mm (Annahme: Größe des Referenzbalkens ist bekannt)
        # Beispielhaft wird hier die Größe als (Breite, Höhe) in mm ausgegeben
        breite_mm = img.shape[1] * referenzbalken_mm / referenzbalken_pixel
        höhe_mm = img.shape[0] * referenzbalken_mm / referenzbalken_pixel
        
        # Ausgabe der Bildgröße
        print(f"Datei: {filename} | Breite: {breite_mm} mm | Höhe: {höhe_mm} mm")

        crp_breite = crp_img_width
        crp_hoehe  = crp_img_height

        # Anzahl der Bilder aus der Bildgröße bestimmen
        anzahl_bilder_x = img.shape[1] // crp_img_width
        anzahl_bilder_y = img.shape[0] // crp_img_height

        # Rand berechnen der auf beiden Seiten freigehalten werden soll, damit alle Bilder mittig reinpassen
        rand_height = (img.shape[0] % crp_img_height) // 2
        rand_width  = (img.shape[1] % crp_img_width) // 2
        
        
''' Bilder zuschneiden '''
# Schleife für jeden Zuschneidebereich
for x in range(anzahl_bilder_x):
    for y in range(anzahl_bilder_y):
        
        os.chdir(path)
        
        # Berechne die Koordinaten des aktuellen Zuschneidebereichs
        crp_x = (x * int(crp_breite)) + rand_width
        crp_y = (y * int(crp_hoehe) ) + rand_height
        
        # Dateiname für den zugeschnittenen Bereich
        crp_name = f"{file_name}_crp_x_{x}_y_{y}.png" 

        # Schneide das Bild entsprechend dem Zuschneidebereich zu
        crp_img = img[crp_y:crp_y+crp_hoehe, crp_x:crp_x+crp_breite]

        # Mittelwerte der Außenkanten berechnen
        mean_top = np.mean(crp_img[0, :])
        mean_bottom = np.mean(crp_img[crp_hoehe - 1 , :])
        mean_right = np.mean(crp_img[:, crp_img_width - 1])
        mean_left = np.mean(crp_img[:,0])

        # Speichere den zugeschnittenen Bereich ab, falls der Mittelwert größer als der Threshold ist
        #img_crp_save_path = crp_img_save_path + crp_name + "all" + ".png"
        #cv2.imwrite(img_crp_save_path, crp_img)

        if mean_top < threshold_edge or mean_bottom < threshold_edge or mean_right < threshold_edge or mean_left < threshold_edge:     
            # Speichere den zugeschnittenen Bereich ab, falls der Mittelwert größer als der Threshold ist
            # Speichere den zugeschnittenen Bereich ab, falls der Mittelwert kleiner oder gleich dem Threshold ist
            img_crp_save_path = os.path.join(crp_img_save_path_rand,crp_name)
            
            # Change the current directory 
            # to specified directory 
            os.chdir(crp_img_save_path)
            
            # Speichere das zugeschnittene Bild
            cv2.imwrite(img_crp_save_path, crp_img)
        else:
            # Speichere den zugeschnittenen Bereich ab, falls der Mittelwert kleiner oder gleich dem Threshold ist
            img_crp_save_path1 = os.path.join(crp_img_save_path,crp_name)
            
            # Change the current directory 
            # to specified directory 
            os.chdir(crp_img_save_path_rand)
            
            # Speichere das zugeschnittene Bild
            cv2.imwrite(img_crp_save_path1, crp_img)