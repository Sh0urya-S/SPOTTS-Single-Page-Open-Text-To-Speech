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

#tek screenshot
time.sleep(2)
pyautogui.screenshot("straight_to_disk.png")
image = cv2.imread("straight_to_disk.png")
cropped_image = image[92:1029, 0:1850]

#test lines for checking if the screenshot is being taken correctly

#cv2.imshow("straight_to_disk.png", imutils.resize(cropped_image, width=1920, height=800))
#cv2.waitKey(0)

#color->greyscale

gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

#specify area to scan

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (941, 1919))

# Applying dilation on the threshold image

dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
 
# Finding contours

contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                 cv2.CHAIN_APPROX_NONE)

# Creating a copy of image
im2 = image.copy()
 
# A text file is created and flushed
file = open("recognized.txt", "w+")
file.write("")
file.close()
 
# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
     
    # Drawing a rectangle on copied image
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
     
    # Cropping the text block for giving input to OCR
    cropped = im2[y:y + h, x:x + w]
     
    # Open the file in append mode
    file = open("recognized.txt", "a")
     
    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped)
     
    # Appending the text into file
    file.write(text)
    file.write("\n")
     
    # Close the file
    #file.close

#extract text from a file and store it in a separate variable

text_file = open("recognized.txt")

with open('recognized.txt', 'r') as file:
    data = file.read().replace('\n', '')
    
#print(data)

tts = gtts.gTTS(data)

tts.save("hello.mp3")

playsound("hello.mp3")

#os.remove("hello.mp3")

#os.remove("recognized.txt")