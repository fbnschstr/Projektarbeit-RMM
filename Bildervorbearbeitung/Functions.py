import os
import cv2 
import numpy as np
import csv
import imutils as imu
import pandas as pd
from matplotlib import pyplot as plt



'''------------------------------------------ ------------------------------------------'''
OPENING_THRESHOLD_DEFAULT = 157

'''------------------------------------------ Ordner erstellen (Funktion) ------------------------------------------'''
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

'''------------------------------------------ Bild drehen (Funktion)------------------------------------------'''
def drehen (save_path, image, angle, filename):
    number_rotations = 360 // angle

    for x in range(number_rotations):
        cal_angle = angle + x * angle
        # Cal steht für calculated

        if cal_angle == 360:
            if filename in os.listdir(save_path):
                # prevent ambigous imgs
                break
            else:
                # do the 360 img
                rotated_img = imu.rotate_bound(image, cal_angle)

                file_name_short = filename[:filename.find('.')]
                rotated_name = f"{file_name_short}_Winkel_{cal_angle}.png"
                #rotated_name = f"{filename}_Winkel_{cal_angle}.png"
                rot_img_save_path = os.path.join(save_path,rotated_name)
                cv2.imwrite(rot_img_save_path, rotated_img)
        else:
            rotated_img = imu.rotate_bound(image, cal_angle)

            file_name_short = filename[:filename.find('.')]
            rotated_name = f"{file_name_short}_Winkel_{cal_angle}.png"

            #rotated_name = f"{filename}_Winkel_{cal_angle}.png"
            rot_img_save_path = os.path.join(save_path,rotated_name)
            cv2.imwrite(rot_img_save_path, rotated_img)

'''------------------------------------------ Rand erkennen (Funktion)------------------------------------------'''
def rand(img, threshold):
    height, width = img.shape
    black_row = False
    black_column = False

    for row in range(height):
        if np.mean(img[row,:]) < threshold:
            black_row = True

    for column in range(width):
        if np.mean(img[:,column]) < threshold:
            black_column = True

    if black_column or black_row:
        return True
    return False

'''------------------------------------------ Porositaet ermitteln (Funktion) ------------------------------------------'''
def getPorositaet(img_path, save_path_closing, save_path_thhold, f, opening_threshold):
    
    # Liste ausgeben, welche Bilddateien im Order abliegen mit dem Befehl os.listdir 
    files = os.listdir(img_path)

    '''Bild-Kernel bestimmen. Die Matrix ist meist eine nxn Matrix und n ist negativ, sodass die Betrachtete Coordinate auch wirklich existiert.
    Kernel beschreibt eine kleine Matrix, die sich in einer großen Bildmatrix fortbewegen kann und somit die Möglichkeit bietet einzelne Koodrinaten
    und dessen Nachbarumgebung zu beschreiben.'''
    kernel = np.ones((5,5),np.uint8)

    # Bild einlesen mit Graufilter in Form einer Schleife für alle Bilddateien, die im Ordner liegen.
    ## for f in files:
    if f.endswith('.png'):
            image_name = f"{f}"

            # Dateiendung abschneiden
            file_name_short = image_name[:image_name.find('.')]
            #print(file_name_short)
            
            # Pfad zum Suchen der Bilder festlegen
            '''mit os.chdir, wird festgelegt in welchem Ordner die Bilder abgespeichert werden können
            Da im Verlauf der Schleife der Speicherort geändert wird, muss er ganz zu Beginn der Schleife wieder zurück auf den Ordner geändert werden,
            in dem die Bilder abliegen, für die die Porösität bestimmt werden soll'''
            os.chdir(img_path)
            
            # Ordnerstruktur erstellen für die Bilddateien, bei dem die Poren vollständig schwarz ausgefüllt sind. 
            file_name = file_name_short + "_closed.png"
            save_path_closing_img = os.path.join(save_path_closing, file_name)
        
            # Öffnen des Bildes
            img = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
            
            # Poren füllen mit dem Opening Befehl, über die Kernel kann eingestellt werden, wie viel schwarz gemacht wird von den Poren.
            opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
            
            # Threshold festlegen, dabei Verwenden von Thresh Binary --> Bild wird nur noch in schwarz und weiß, keine graustufen dargestellt.
            ret,th1 = cv2.threshold(opening,opening_threshold,255,cv2.THRESH_BINARY)
            
            # Zählen der Pixel, die schwarz und weiß sind. 
            # Zählen wird mit dem threshold-Bild durchgeführt, da es hier nur noch schwarz und weiß gibt.
            white_pixel = np.sum(th1 == 255)
            black_pixel = np.sum(th1 == 0)
    
            #print('Number of white pixels:', white_pixel)
            #print('Number of black pixels:', black_pixel)
            
            # Berechnen der gesamten Pixel im Bild
            y_th1, x_th1 = th1.shape
            #print("Breite des Zuschnitts in Pixel:", x_th1)
            #print("Höhe des Zuschnitts in Pixel:", y_th1)
            ges_pixel = x_th1 * y_th1
            #print("Gesamtanzahl Pixel:", ges_pixel)
                
            # Berechnen der Poroesitaet in Prozent
            poroesitaet = (black_pixel/ges_pixel) * 100
            ##poroesitaet_round = round(poroesitaet, 3)
            #print("Poroesität der Probe in %",poroesitaet)
            dichte = (white_pixel/ges_pixel) * 100
            #print("Dichte der Probe in %",dichte) 
            
            ''' optional: # plotten Threshold --> Wird der Wert 200 nach oben verschoben, können auch die schwarzen Anteile nach oben verschoben werden. 
            titles = ['Opening', 'Th1']
            images = [opening, th1]
            
            for i in range(2):
                plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
                plt.title(titles[i])
                plt.show()'''
        
            # Dateinamen mit Poroesitaet
            file_name_th1 = f"{file_name_short}_Por_{poroesitaet}.png"
            #file_name_th1 = f"{file_name_short}_Por_{poroesitaet_round}.png"

            #file_name_th1 = f"{image_name}_Por_{poroesitaet}.png"
            save_path_thhold_img = os.path.join(save_path_thhold, file_name_th1)
            #print("save_path_thhold_img:",save_path_thhold_img)   
        
            #Bild abspeichern unter dem Namen closed_'Dateiname'.png 
            # os.chdir(save_path_closing)
            # cv2.imwrite(save_path_closing_img, opening)
            
            # os.chdir(save_path_thhold)        
            # cv2.imwrite(save_path_thhold_img, th1)
            
            '''if not os.path.exists(save_path_closing_img):
                cv2.imwrite(file_name, opening)
                os.rename(save_path_old, save_path_closing_img)'''
    
    # Rückgabe des Porositaetswertes       
    return poroesitaet
    ##return poroesitaet_round
            
        
