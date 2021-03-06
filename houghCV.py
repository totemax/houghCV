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
  
  for i in range(0, len(posibles[0])):
    if posibles[2][i] > 0:
      votesIndex = resultsMatrix[posibles[0][i], posibles[1][i], posibles[2][i]] / posibles[2][i]
      if votesIndex > primero[0]:
	segundo = primero
	primero = (votesIndex, posibles[0][i], posibles[1][i], posibles[2][i])
      elif votesIndex > segundo[0]:
	segundo = (votesIndex, posibles[0][i], posibles[1][i], posibles[2][i])
  
  return primero, segundo
  


#leemos la imagen de los argumentos pasados por linea de comandos
img_file = sys.argv[1]

img = cv2.imread(img_file)

cv2.imshow('image',img)

#extraemos el segmento de la imagen que contiene los ojosq
eyes_segment = img[30:60, 12:79]

eyes_gray = eyes_segment

#cambiamos su espacio de colores a escala de grises
cv2.cvtColor( eyes_segment, cv2.COLOR_BGR2GRAY, eyes_gray);

#realizamos una umbralización
ret, eyes_binarized = cv2.threshold(eyes_gray,110,255,cv2.THRESH_BINARY_INV)

cv2.imshow('umbralizada',eyes_binarized)

mask = np.ones([3,3], np.uint8)

circle_mask = np.ones([5,5], np.uint8)

circle_mask[0][0] = 0;
circle_mask[1][0] = 0;
circle_mask[0][1] = 0;
circle_mask[3][0] = 0;
circle_mask[4][0] = 0;
circle_mask[4][1] = 0;
circle_mask[0][3] = 0;
circle_mask[0][4] = 0;
circle_mask[1][4] = 0;
circle_mask[4][3] = 0;
circle_mask[3][4] = 0;
circle_mask[4][4] = 0;

eyes_binarized = cv2.dilate(eyes_binarized, mask, iterations = 1)

#cv2.imshow('primera dilatacion',eyes_binarized)

eyes_binarized = cv2.erode(eyes_binarized, mask, iterations = 1)

#cv2.imshow('primera erosion',eyes_binarized)

eyes_binarized = cv2.erode(eyes_binarized, circle_mask, iterations = 1)

#cv2.imshow('segunda erosion',eyes_binarized)

eyes_binarized = cv2.dilate(eyes_binarized, circle_mask, iterations = 1)

cv2.imshow('segunda dilatacion',eyes_binarized)

eyes_binarized = cv2.morphologyEx(eyes_binarized, cv2.MORPH_OPEN, circle_mask)

cv2.imshow('primera apertura',eyes_binarized)

eyes_binarized = cv2.morphologyEx(eyes_binarized, cv2.MORPH_CLOSE, circle_mask)

cv2.imshow('primer cierre',eyes_binarized)

#eyes_binarized = cv2.erode(eyes_binarized, mask, iterations = 1)

dilate = cv2.dilate(eyes_binarized, mask, iterations = 1)

eyes_binarized = dilate - eyes_binarized

cv2.imshow('ojos',eyes_binarized)

primero, segundo = houghCircleTransform(eyes_binarized)

cv2.circle(eyes_segment, (primero[1], primero[2]), primero[3] + 2, (0,255,0), 1)
cv2.circle(eyes_segment, (segundo[1], segundo[2]), segundo[3] + 2, (0,255,0), 1)

img[30:60, 12:79] = eyes_segment

cv2.imshow('resultado',img)

k = cv2.waitKey(0) & 0xFF
while k != ord('q'):
    k = cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()

