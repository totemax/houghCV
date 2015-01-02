#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sys

def houghCircleTransform(img):
  "Cálculo de la tranformada de hough para una circunferencia"
  height = img.shape[0]
  width = img.shape[1]
  resultsMatrix = np.zeros([width, height, width*height], np.uint8)
  whites = np.where(img > 0)
  for pixel in range(0,len(whites[0])):
    for i in range(0, width):
      for j in range(0, height):
	r = (((whites[0][pixel] - j)**2) + ((whites[1][pixel] - i)**2))**0.5
	resultsMatrix[i, j, r] += 1
  
  primero = (0,0,0,0)
  segundo = (0,0,0,0)
  posibles = np.where(resultsMatrix > 1)
  return posibles
  


#leemos la imagen de los argumentos pasados por linea de comandos
img_file = sys.argv[1]

img = cv2.imread(img_file)

cv2.imshow('image',img)

#extraemos el segmento de la imagen que contiene los ojos
eyes_segment = img[30:60, 15:77]

eyes_gray = eyes_segment

#cambiamos su espacio de colores a escala de grises
cv2.cvtColor( eyes_segment, cv2.COLOR_BGR2GRAY, eyes_gray);

#realizamos una umbralización
ret, eyes_binarized = cv2.threshold(eyes_gray,125,255,cv2.THRESH_BINARY_INV)

cv2.imshow('umbralizada',eyes_binarized)

mask = np.ones([3,3], np.uint8)

dilate_mask = np.ones([3,3], np.uint8)

dilate_mask[0][0] = 0;
dilate_mask[2][0] = 0;
dilate_mask[0][2] = 0;
dilate_mask[2][2] = 0;

eyes_binarized = cv2.erode(eyes_binarized, mask, iterations = 1)

cv2.imshow('primer_cierre',eyes_binarized)

eyes_binarized = cv2.dilate(eyes_binarized, dilate_mask, iterations = 1)

#eyes_binarized = cv2.morphologyEx(eyes_binarized, cv2.MORPH_OPEN, dilate_mask)

#eyes_binarized = cv2.erode(eyes_binarized, mask, iterations = 1)

dilate = cv2.dilate(eyes_binarized, mask, iterations = 1)

eyes_binarized = dilate - eyes_binarized

cv2.imshow('ojos',eyes_binarized)

posibles = houghCircleTransform(eyes_binarized)

for circle in range(0, len(posibles[0])):
  cv2.circle(eyes_segment, (posibles[0][circle], posibles[1][circle]), posibles[2][circle] + 2, (0,255,0), 1)

img[30:60, 15:77] = eyes_segment

cv2.imshow('resultado',img)

k = cv2.waitKey(0) & 0xFF
while k != ord('q'):
    k = cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()

