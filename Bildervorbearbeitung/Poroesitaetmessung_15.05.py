import os
import cv2 
import numpy as np
from matplotlib import pyplot as plt


# Pfad der aktuellen Datei
path = os.path.dirname(__file__)
img_path = os.path.join(path, "Zugeschnittene_Bilder")
#print(img_path)
if not os.path.exists(img_path):
        os.mkdir(img_path)

save_path_closing = os.path.join(path, "Bilder_Closed")
#print(save_path_closing)
if not os.path.exists(save_path_closing):
    os.mkdir(save_path_closing)

save_path_thhold = os.path.join(save_path_closing, "Threshold")
#print(save_path_thhold)
if not os.path.exists(save_path_thhold):
        os.mkdir(save_path_thhold)

#Liste ausgeben, welche Bilddateien im Order abliegen mit dem Befehl os.listdir 
files = os.listdir(img_path)

'''Bild-Kernel bestimmen. Die Matrix ist meist eine nxn Matrix und n ist negativ, sodass die Betrachtete Coordinate auch wirklich existiert.
Kernel beschreibt eine kleine Matrix, die sich in einer großen Bildmatrix fortbewegen kann und somit die Möglichkeit bietet einzelne Koodrinaten
und dessen Nachbarumgebung zu beschreiben.'''
kernel = np.ones((5,5),np.uint8)

#Bild einlesen mit Graufilter in Form einer Schleife für alle Bilddateien, die im Ordner liegen.
for f in files:
    if f.endswith('.png'):
        image_name = f"{f}"
         
        #Pfad zum Suchen der Bilder festlegen
        os.chdir(img_path)

        # Ordnerstruktur erstellen für die Bilddateien, bei dem die Poren vollständig scharz ausgefüllt sind. 
        file_name = "closed_"+ image_name
        #save_path_old =  os.path.join(path, file_name)
        save_path_closing_img = os.path.join(save_path_closing, file_name)
        print("Save_path_closing_img:", save_path_closing_img)
    
        #Öffnen des Bildes
        img = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
        
        #Poren füllen mit dem Opening Befehl, über die Kernel kann eingestellt werden, wie viel schwarz gemacht wird von den Poren.
        opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        
        # Threshold festlegen, dabei Verwenden von Thresh Binary --> Bild wird nur noch in schwarz und weiß, keine graustufen dargestellt.
        ret,th1 = cv2.threshold(opening,185,255,cv2.THRESH_BINARY)
        
        #Zählen der Pixel, die schwarz und weiß sind. 
        #Zählen wird mit dem threshold-Bild durchgeführt, da es hier nur noch schwarz und weiß gibt.
        white_pixel = np.sum(th1 == 255)
        black_pixel = np.sum(th1 == 0)
  
        print('Number of white pixels:', white_pixel)
        print('Number of black pixels:', black_pixel)
        
        #Berechnen der gesamten Pixel im Bild
        y_th1, x_th1 = th1.shape
        print("Breite des Zuschnitts in Pixel:", x_th1)
        print("Höhe des Zuschnitts in Pixel:", y_th1)
        ges_pixel = x_th1 * y_th1
        print("Gesamtanzahl Pixel:", ges_pixel)
            
        #Berechnen der Poroesitaet in Prozent
        poroesitaet = (black_pixel/ges_pixel)*100
        print("Poroesität der Probe in %",poroesitaet)
        dichte = (white_pixel/ges_pixel)*100
        print("Dichte der Probe in %",dichte)
         
        ''' optional: # plotten Threshold --> Wird der Wert 200 nach oben verschoben, können auch die schwarzen Anteile nach oben verschoben werden. 
        titles = ['Opening', 'Th1']
        images = [opening, th1]
        
        for i in range(2):
            plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
            plt.title(titles[i])
            plt.show()'''
    
    #Dateinamen mit Poroesitaet
        file_name_th1 = f"{image_name}_Por_{poroesitaet}.png"
        save_path_thhold_img = os.path.join(save_path_thhold, file_name_th1)
        print("save_path_thhold_img:",save_path_thhold_img)   
    
        #Bild abspeichern unter dem Namen closed_'Dateiname'.png 
        os.chdir(save_path_closing)
        cv2.imwrite(save_path_closing_img, opening)
        
        os.chdir(save_path_thhold)        
        cv2.imwrite(save_path_thhold_img, th1)
      