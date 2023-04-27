# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 19:20:19 2023

@author: marys
"""

'''import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image


Versuchsbild = mpimg.imread('Versuchsbild.png')
width, height = Versuchsbild.size
plt.axis("off")
imgplot = plt.imshow(Versuchsbild)'''


import os

from PIL import Image

image_name = 'Bild.png'
img = Image.open(image_name)

breite = img.width
hoehe = img.height
print("Breite Übersichtsbild:",breite)
print("Höhe Übersichtsbild:", hoehe)

# Zugeschnitte Bildgröße definieren
crp_breite = 500
crp_hoehe = 500

# Anzahl der Bilder, die zugeschnitten werden sollen und Berechnung des Rands für die Bilder:
"""Rechenzeichen für Division: 
     -> / steht für die ganz normale Divison z.B. 3/2 = 1,5
     -> % errechnet den Rest: z.B. bei 3%2 = 0,5, da die 2 1x in die 3 geht Rest 0,5
     -> // errechnet die ganzzahlige Zahl die noch in den Zähler pass: z.B. 3/2 = 1"""
     
anzahl_x = breite//crp_breite
rand_x = (breite%crp_breite)/2
anzahl_y = hoehe//crp_hoehe
rand_y = (hoehe%crp_hoehe)/2
print("Anzahl der Bilder in x-Richtung:", anzahl_x)
print("Rand in jede x-Richtung in Pixel:",rand_x )
print("Anzahl der Bilder in y-Richtung:", anzahl_y)
print("Rand in jede y-Richtung in Pixel:",rand_y )


# Schleife zum Zuschneider der Bilder: zunächst festlegen der Koordinaten
""" Erklärung: Zuschneiden des Bilds von der Anfangskoodinate crp_startcoord 
bis in einer bestimmten Größe crp_breite und crp_höhe --> Berechnen der Endkoordinte aus Anfangskoordinate
und vorgegebnenen Größen
Der Befehl img.crop schneidet dabei das Bild zu. Dabei ist es wichtig, dass vorne und hinten zwei Klammern gesetzt werden.
Das der Befehl eigentlich nur mit einer Variablen box funktioniert. Mit den zweiten Klammern wird ein Argument nachgebildet."""
for x in range(anzahl_x):
    for y in range(anzahl_y):
        crp_startcoord_x = rand_x + (x*crp_breite)
        crp_startcoord_y = rand_y + (y*crp_hoehe)
        crp_Bild = img.crop((crp_startcoord_x,crp_startcoord_y,crp_startcoord_x+crp_breite,crp_startcoord_y+crp_hoehe))
        
        crp_name = f"{image_name}Zuschnitt{y}{x}"
        
        crp_Bild.save(os.path.join(crp_name+".png"))
        