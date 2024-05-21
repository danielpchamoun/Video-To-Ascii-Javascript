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

jsoutput = open("animation.js","w")  #clearing javascript file
jsoutput.write("")
jsoutput.close()

count = 0
colorFrames =  []
asciiFrames = []

windowW = 0
windowH = 0
while cap.isOpened():
    ret, frame = cap.read() #gets next frame
    if ret:
        resized = cv.resize(frame, None, fx=factorX, fy=factorY, interpolation=cv.INTER_CUBIC)

    height = int(resized.shape[0])
    width = int(resized.shape[1])
    windowW = width
    windowH = height
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY) #also the same as intensity
    colorValues = []
    asciiValues = []
    for y in range(height):
        asciiRow = []
        colorRow = []
        for x in range(width):
            color = resized[y,x].tolist()
            ascii = ascii_ramp[int((gray[y,x]*69)/255)]
            colorRow.append(color)
            asciiRow.append(ascii)
        colorValues.append(colorRow)
        asciiValues.append(asciiRow)
    asciiFrames.append(asciiValues)
    colorFrames.append(colorValues)
    


    print(str(count) + "/" +str(int(cap.get(cv.CAP_PROP_FRAME_COUNT))))

    count+=1
    cv.imshow('resized', gray)
    if cv.waitKey(1) == ord('q'):
        break
    os.system('cls')
#print(asciiValues)
#print(colorValues)
jsoutput = open("animation.js","a")

jsoutput.write("colorValues ="+str(colorFrames)+";\n")
jsoutput.write("asciiValues ="+str(asciiFrames)+";\n")
jsoutput.write("const canvas = document.getElementById(\"asciianimation\");\n")
jsoutput.write("const ctx = canvas.getContext(\"2d\");\n")
jsoutput.write("var frameIndex = 0;\n")
jsoutput.write("var interval = window.setInterval(function(){\n")
jsoutput.write("frameIndex += 1;\n")
jsoutput.write("ctx.clearRect(0, 0, canvas.width, canvas.height);\n")
jsoutput.write("for(let i = 0; i < "+str(windowH)+"; i++){\n")
jsoutput.write("    for(let j = 0; j < "+str(windowW)+"; j++){\n")
jsoutput.write("        ctx.font = \"20px Courier New, monospace\";\n")
jsoutput.write("        ctx.fillStyle = \"rgb(\"+String(colorValues[frameIndex][i][j][2])+\",\"+String(colorValues[frameIndex][i][j][1])+\",\"+String(colorValues[frameIndex][i][j][0])+\")\";\n")
jsoutput.write("        ctx.fillText(asciiValues[frameIndex][i][j],j*16,i*16); // might need to change starting location here\n") 
jsoutput.write("    }\n")
jsoutput.write("}\n")

jsoutput.write("if(frameIndex == "+str(int(cap.get(cv.CAP_PROP_FRAME_COUNT)-1))+"){\n")
jsoutput.write("    frameIndex = 0;\n")
jsoutput.write("}\n")
jsoutput.write("}, 2);\n")
jsoutput.close()

cap.release()
cv.destroyAllWindows()