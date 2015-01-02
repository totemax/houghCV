#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np

def houghCircleTransform(img):
  "Cálculo de la tranformada de hough para una circunferencia"
  height = img.shape[0]
  width = img.shape[1]
  resultsMatrix = np.zeros([width, height, max(width, height)], np.uint8)
  whites = np.where(img > 0)
  for pixel in range(0,len(whites[0])):
    for i in range(0, width):
      for j in range(0, height):
	r = (((whites[0][pixel] - j)**2) + ((whites[1][pixel] - i)**2))**0.5
	resultsMatrix[i, j, r] += 1
  print len(np.where(resultsMatrix > 0)[0])
  
  maximo = (0,0,0,0)
  posibles = np.where(resultsMatrix > 0)
  for circle in range(0, len(posibles[0])):
    if maximo[0] < resultsMatrix[posibles[0][circle], posibles[1][circle], posibles[2][circle]]:
      maximo = (resultsMatrix[posibles[0][circle], posibles[1][circle], posibles[2][circle]], posibles[0][circle], posibles[1][circle], posibles[2][circle])
    elif maximo[0] == resultsMatrix[posibles[0][circle], posibles[1][circle], posibles[2][circle]] and maximo[3] < posibles[2][circle]:
      maximo = (resultsMatrix[posibles[0][circle], posibles[1][circle], posibles[2][circle]], posibles[0][circle], posibles[1][circle], posibles[2][circle])
  return maximo
  


# Create a black image
img = np.zeros((50,50, 3), np.uint8)

cv2.circle(img,(25,25), 10, (255,255,255), -1)



mask = np.ones([3,3], np.uint8)
erode = cv2.erode(img, mask, iterations = 1)
img2 = img - erode;

cv2.cvtColor( img2, cv2.COLOR_BGR2GRAY);

circle = houghCircleTransform(img2)

cv2.circle(img, (circle[1], circle[2]), circle[3] + 2, (0,255,0), 1)

cv2.imshow('borde', img2)
cv2.imshow('image',img)

k = cv2.waitKey(0) & 0xFF
while k != ord('q'):
    k = cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()

