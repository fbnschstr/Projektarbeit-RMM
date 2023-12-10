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
        return pfad_ersteller_ordner
    
    os.mkdir(pfad_ersteller_ordner)

    return pfad_ersteller_ordner

'''------------------------------------------ Bild drehen (Funktion)------------------------------------------'''
def drehen (save_path: str, save_path_col: str, image: float, angle: float, filename: str, save_color_version: bool):
    number_rotations = 360 // angle
    rotated_img_list = []

    for x in range(number_rotations):
        cal_angle = angle + x * angle
        # Cal steht für calculated

        file_name_short = filename[:filename.find('.')]
        rotated_name = f"{file_name_short}_Winkel_{cal_angle}.png"
        rot_img_save_path = os.path.join(save_path,rotated_name)

        if cal_angle == 360:
            if filename in os.listdir(save_path):
                # prevent ambigous imgs
                break
            else:
                # do the 360 img
                rotated_img = imu.rotate_bound(image, cal_angle)
                rotated_img_list.append(rotated_name)

        else:
            rotated_img = imu.rotate_bound(image, cal_angle)
            rotated_img_list.append(rotated_name)
        
        if save_color_version == True:
            rotated_name_col = f"{file_name_short}_Winkel_{cal_angle}_col.png"
            rot_img_save_path_color = os.path.join(save_path_col, rotated_name_col)
            image = cv2.cvtColor(rotated_img, cv2.COLOR_GRAY2BGR)
            cv2.imwrite(rot_img_save_path_color, image)
        else:
            cv2.imwrite(rot_img_save_path, rotated_img)

    return rotated_img_list
'''------------------------------------------ Rand erkennen (Funktion)------------------------------------------'''
def rand(img, threshold):
    height, width = img.shape

    for row in range(height):
        if np.mean(img[row,:]) < threshold:
            return True 
    
    for column in range(width):
        if np.mean(img[:,column]) < threshold:
            return True
    
    return False

'''------------------------------------------ Porositaet ermitteln (Funktion) ------------------------------------------'''
def getPorositaet(image, opening_threshold):

    '''Bild-Kernel bestimmen. Die Matrix ist meist eine nxn Matrix und n ist negativ, sodass die Betrachtete Coordinate 
    auch wirklich existiert. Kernel beschreibt eine kleine Matrix, die sich in einer großen Bildmatrix fortbewegen 
    kann und somit die Möglichkeit bietet einzelne Koodrinaten und dessen Nachbarumgebung zu beschreiben.'''
    kernel = np.ones((5,5),np.uint8)
    
    # Poren füllen mit dem Opening Befehl, über die Kernel kann eingestellt werden, wie viel schwarz gemacht wird von den Poren.
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    
    # Threshold festlegen, dabei Verwenden von Thresh Binary --> Bild wird nur noch in schwarz und weiß, keine graustufen dargestellt.
    ret,th1 = cv2.threshold(opening,opening_threshold,255,cv2.THRESH_BINARY)

    # Zählen der Pixel, die schwarz und weiß sind
    #white_pixel = np.sum(th1 == 255)
    black_pixel = np.sum(th1 == 0)
    
    # Berechnen der gesamten Pixel im Bild
    y_th1, x_th1 = th1.shape

    ges_pixel = x_th1 * y_th1

    # Berechnen der Poroesitaet in Prozent
    poroesitaet = (black_pixel/ges_pixel) * 100

    # Rückgabe des Porositaetswertes       
    return poroesitaet

'''------------------------------------------ Klassen erstellen ------------------------------------------'''
def get_class (porosity):
    thresholds_narrow = np.arange(0.01, 1.5, 0.01)
    threshold_middle = np.arange(1.5,10.5,0.5)
    threshold_wide = np.arange(20,110,10)
    thresholds = np.concatenate((thresholds_narrow, threshold_middle, threshold_wide))

    for i, threshold in enumerate(thresholds, start=1):
        if porosity <= threshold:
            return i
    return len(thresholds)