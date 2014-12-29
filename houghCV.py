#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np

# Create a black image
img = np.zeros((512,512,3), np.uint8)

cv2.circle(img,(256,256), 128, (255,255,255), -1)

cv2.imshow('image',img)
k = cv2.waitKey(0) & 0xFF
while k != ord('q'):
    k = cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()