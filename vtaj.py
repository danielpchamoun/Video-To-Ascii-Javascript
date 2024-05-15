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

if len(sys.argv) < 2:     
    print("Error. Wrong number of arguments.")
    sys.exit(1)

outputfile = "video.mp4"

youtubeLink = sys.argv[1] #might need to swap these two arguments, user should be able to simply add either youtube video or direct mp4 to convert to ascii

if len(sys.argv) == 3:
    outputfile = sys.argv[2]
print("Downloading video from: "+youtubeLink)

yt = YouTube(youtubeLink)

#get highest quality video from stream list
mp4 = yt.streams.get_highest_resolution()

try:
    mp4.download(filename=outputfile)
except:
    print("Download Failed")
inputHeight = 100
inputWidth = 100
cap = cv.VideoCapture('outputvid.mp4')
cap.set(3, inputWidth)
cap.set(4, inputHeight)

# 70 levels of gray
ascii_ramp = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "



ret, frame = cap.read()

height = int(frame.shape[0])
width = int(frame.shape[1])



cv.resize(frame, (width,height), interpolation =cv.INTER_AREA)


cmd = 'mode '+str(width)+','+ str(height)
os.system(cmd)


while cap.isOpened():
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #also the same as intensity
    asciiframe=""
    for y in range(height):
        asciiframe+= "\n"
        for x in range(width):
            color = frame[y,x]
            ascii = ascii_ramp[int((gray[y,x]*69)/255)]
            asciiframe += ascii
    os.system('cls')

    print(asciiframe)



    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
 
cap.release()
cv.destroyAllWindows()