from PIL import Image
import gtts
from gtts import gTTS
from playsound import playsound
import os
import numpy as np
import pyautogui
import imutils
import cv2
import time
import pytesseract

time.sleep(2)
pyautogui.screenshot("straight_to_disk.png")
image = cv2.imread("straight_to_disk.png")
cropped_image = image[92:1029, 0:1850]

gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (941, 1919))

dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
 
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                 cv2.CHAIN_APPROX_NONE)

im2 = image.copy()
 
file = open("recognized.txt", "w+")
file.write("")
file.close()
 
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
     
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
     
    cropped = im2[y:y + h, x:x + w]
     
    file = open("recognized.txt", "a")
     
    text = pytesseract.image_to_string(cropped)
     
    file.write(text)
    file.write("\n")
     
text_file = open("recognized.txt")

with open('recognized.txt', 'r') as file:
    data = file.read().replace('\n', '')
    
tts = gtts.gTTS(data)

tts.save("hello.mp3")

playsound("hello.mp3")
