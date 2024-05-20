#https://github.com/pytube/pytube
#https://www.geeksforgeeks.org/converting-image-ascii-image-python/
#python -m pip install --upgrade pip
#python -m pip install pytube
#python -m pip install opencv-python

#later if I want to add a webcam, might need to configure using the VideoCapture class within OpenCV

import os, sys
import cv2 as cv
from PIL import Image
from pytube import YouTube
from tkinter import *
from tkinter import ttk
import array
import numpy

#do GUI stuff after color
#root = Tk()
#frm = ttk.Frame(root, padding=10)
#frm.grid()
#ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
#ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
#root.mainloop()

if len(sys.argv) != 2:     
    print("Error. Wrong number of arguments.")
    sys.exit(1)


youtubeLink = sys.argv[1] #might need to swap these two arguments, user should be able to simply add either youtube video or direct mp4 to convert to ascii




#get highest quality video from stream list

inputfile = sys.argv[1]

if inputfile.startswith("https://"): 
    print("Downloading video from: "+youtubeLink)
    yt = YouTube(youtubeLink)
    mp4 = yt.streams.get_highest_resolution()
    mp4.download(filename="video.mp4")

cap = cv.VideoCapture("video.mp4")


# 70 levels of gray
ascii_ramp = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "



factorX = 0.08 #change to user inputs 
factorY = 0.08 #change to user inputs 

jsoutput = open("animation.js","w") 
jsoutput.write("asciiframes = [")
jsoutput.close()

count = 0
asciiValues = []
colorValues =  []
while cap.isOpened():
    ret, frame = cap.read() #gets next frame
    if ret:
        resized = cv.resize(frame, None, fx=factorX, fy=factorY, interpolation=cv.INTER_CUBIC)

    height = int(resized.shape[0])
    width = int(resized.shape[1])
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY) #also the same as intensity
    asciiframe=""    
    for y in range(height):
        asciiValues.append([])
        colorValues.append([])
        for x in range(width):
            color = resized[y,x]
            ascii = ascii_ramp[int((gray[y,x]*69)/255)]
            asciiValues[y].append(ascii)
            colorValues[y].append(color)
            asciiframe += ascii
        asciiframe+= "\n" #for seeing it in the console

    
    jsoutput = open("animation.js","a") 

    jsoutput.close()

    print(str(count) + "/" +str(int(cap.get(cv.CAP_PROP_FRAME_COUNT))))

    count+=1
    cv.imshow('resized', gray)
    if cv.waitKey(1) == ord('q'):
        break
    os.system('cls')


for i in range len(colorValues):
    for j in range(len(colorValues[i])):


jsoutput = open("animation.js","a")
jsoutput.write("const canvas = document.getElementById("asciianimation");\nconst ctx = canvas.getContext(\"2d\");\nctx.font = \"50px Courier New, monospace\";\nctx.fillStyle = \"rgb("str(colorValues[i][j][0])","+str(colorValues[i][j][1])+","+str(colorValues[i][j][2])+")\";\nctx.fillText(asciiValues[i][j],10,80);\nasciiFrameIndex = 0;\nvar asciiInterval = window.setInterval(function(){asciiFrameIndex += 1;\ndocument.getElementById(\"asciianimation\").innerHTML = asciiframes[asciiFrameIndex];\n")
jsoutput.write("")
jsoutput.close()

cap.release()
cv.destroyAllWindows()