#https://github.com/pytube/pytube
#https://www.geeksforgeeks.org/converting-image-ascii-image-python/
#python -m pip install --upgrade pip
#python -m pip install pytube
#python -m pip install opencv-python

#later if I want to add a webcam, might need to configure using the VideoCapture class within OpenCV

import os, sys
import cv2 as cv
import tkinter.filedialog
from PIL import Image
from pytube import YouTube
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
import array
import numpy


# Function that will be invoked when the
# button will be clicked in the main window
userCustomColor="red"
def choose_color():
    global userCustomColor
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor(title ="Choose color") 
    userCustomColor = color_code[1] #do more splitting here
    selectedColorButton.config(bg=userCustomColor, text="Selected Color: " + userCustomColor)
    return

userVideoInput = ""
def choose_file():
    file_path = tkinter.filedialog.askopenfilename(filetypes=(("Video files", "*.mp4;"),("All files", "*.*") ))
    print("Selected file path:", file_path)
    
    selectedFileEntry.delete(0, END)
    selectedFileEntry.insert(0, file_path)
    selectedFileEntry.config(fg='black')

    return


def selectedFileEntryFocus(event):
    if selectedFileEntry.get() == 'Enter file path or paste YouTube link here':
        selectedFileEntry.delete(0, END)
        selectedFileEntry.insert(0, '')
        selectedFileEntry.config(fg='black')

def selectedFileEntryUnfocus(event):
    if selectedFileEntry.get() == '':
        selectedFileEntry.insert(0, 'Enter file path or paste YouTube link here')
        selectedFileEntry.config(fg='grey')

def startEntryFocus(event):
    if startEntry.get() == '00:00:00':
        startEntry.delete(0, END)
        startEntry.insert(0, '')
        startEntry.config(fg='black')

def startEntryUnfocus(event):
    if startEntry.get() == '':
        startEntry.insert(0, '00:00:00')
        startEntry.config(fg='grey')



def main():

    userVideoInput = selectedFileEntry.get()
    print(userVideoInput)
    if userVideoInput.startswith("https://"):
        print("Downloading video from: " + userVideoInput)
        try:
            yt = YouTube(userVideoInput)
            mp4 = yt.streams.get_highest_resolution()
            mp4.download(filename="video.mp4")
            inputfile = "video.mp4"
            print("Video downloaded successfully.")
        except Exception as e:
            print("Error downloading video:", e)
            return
    else:
        inputfile = userVideoInput
    print(inputfile)
    cap = cv.VideoCapture(inputfile)
    if not cap.isOpened():
        print("Error: Couldn't open video file.")
        return

    fps = cap.get(cv.CAP_PROP_FPS)

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

    #time parameters
    startTime = startEntry.get()
    endTime = endEntry.get()

    if startTime:
        startSeconds = int(startTime[0:2]) * 3600 + int(startTime[3:5]) * 60 + int(startTime[6:8])
    else:
        startSeconds = 0

    if endTime:
        endSeconds = int(endTime[0:2]) * 3600 + int(endTime[3:5]) * 60 + int(endTime[6:8])
    else:
        endSeconds = int(cap.get(cv.CAP_PROP_FRAME_COUNT) / fps)

    while cap.isOpened():
        ret, frame = cap.read() #gets next frame
        if not ret or count / fps >= endSeconds:
            print("Done.")
            break
        
        if count / fps >= startSeconds:
            resized = cv.resize(frame, None, fx=factorX, fy=factorY, interpolation=cv.INTER_CUBIC)
            height = int(resized.shape[0])
            width = int(resized.shape[1])
            windowW = width
            windowH = height

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

            #update with new time later
            print("Converting:" + str(min(100, round((count / (fps * endSeconds)) * 100, 2)))+"%")

        count+=1
        cv.imshow('resized', gray)
        if cv.waitKey(1) == ord('q'):
            break

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
    sys.exit(1)



#do GUI stuff after color
root = Tk()
root.title("Javascript Ascii Animation Converter")
root.geometry("510x100")
root.resizable(False, False)
frm = ttk.Frame(root, padding=2.5)
frm.grid()


ttk.Button(frm, text="Browse", command=choose_file).grid(column=1, row=1, sticky="w")
selectedFileEntry = ttk.Entry(frm, width=55)
selectedFileEntry.grid(column=0, row=1)

startEntry = Entry(frm, width=10,fg='grey')
startEntry.insert(0, '00:00:00')
startEntry.bind('<FocusIn>', startEntryFocus)
startEntry.bind('<FocusOut>', startEntryUnfocus)

startEntry.grid(column=1, row=3,sticky="w")


startLabel = Label(frm, text="Start")
startLabel.grid(column=1, row=4 ,sticky="w")

endEntry = ttk.Entry(frm, width=10)
endEntry.grid(column=2, row=3, sticky="w")

endLabel = Label(frm, text="End")
endLabel.grid(column=2, row=4, sticky="w")

selectedColorButton = Button(frm, text="Selected Color: #ffffff", command=choose_color, bg = "#ffffff")
selectedColorButton.grid(column=0, row=3)


#use colorFilterEnabled.get() to see if checked or unchecked
colorFilterEnabled = BooleanVar()
autoDownloadCheckbox = Checkbutton(frm, text="Enable Color Filter", variable=colorFilterEnabled)
autoDownloadCheckbox.grid(column=0, row=4)
ttk.Button(frm, text="Convert Video", command=main).grid(column=2, row=1,sticky="w")


selectedFileEntry = Entry(frm, width=55, fg='grey')
selectedFileEntry.insert(0, 'Enter file path or paste YouTube link here')
selectedFileEntry.bind('<FocusIn>', selectedFileEntryFocus)
selectedFileEntry.bind('<FocusOut>', selectedFileEntryUnfocus)
selectedFileEntry.grid(column=0, row=1)

root.mainloop()

