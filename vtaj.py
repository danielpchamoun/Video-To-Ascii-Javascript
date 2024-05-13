#https://github.com/pytube/pytube
#python -m pip install --upgrade pip
#python -m pip install pytube
#python -m pip install opencv-python

#later if I want to add a webcam, might need to configure using the VideoCapture class within OpenCV
import os, sys
import cv2
from PIL import Image
from pytube import YouTube

if len(sys.argv) > 3: #change to 3 if i need an additional argument for the mp4 file later    
    print("Error. Wrong number of arguments.")
    sys.exit(1)

youtubeLink = sys.argv[1] #might need to swap these two arguments, user should be able to simply add either youtube video or direct mp4 to convert to ascii

print(youtubeLink)

yt = YouTube(youtubeLink)

#get highest quality video from stream list
mp4 = yt.streams.get_highest_resolution()


try:
    mp4.download()
except:
    print("Download Failed")