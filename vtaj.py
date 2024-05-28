#https://github.com/pytube/pytube
#https://www.geeksforgeeks.org/converting-image-ascii-image-python/
#python -m pip install --upgrade pip
#python -m pip install pytube
#python -m pip install opencv-python
#python -m pip install imageio

#later if I want to add a webcam, might need to configure using the VideoCapture class within OpenCV

import os, sys
import cv2 as cv
import tkinter.filedialog
from PIL import Image as PILimg
from PIL import ImageDraw
from PIL import ImageFont

from pytube import YouTube
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import StringVar
from tkinter import OptionMenu


import array
import numpy as np
import math
import imageio



# Function that will be invoked when the
# button will be clicked in the main window
userCustomColor= (0,0,0)
def chooseColor():
    global userCustomColor
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor(title ="Choose color") 
    userCustomColor = color_code[0] #do more splitting here
    selectedColorButton.config(bg=color_code[1]) #, text=str(color_code[1][1:])
    return

userVideoInput = ""
def chooseFile():
    file_path = tkinter.filedialog.askopenfilename(filetypes=(("Video files", "*.mp4;"),("All files", "*.*") ))    
    selectedFileEntry.delete(0, END)
    selectedFileEntry.insert(0, file_path)
    selectedFileEntry.config(fg='black')
    return


def applyColorFilter(frame, color):
    b, g, r = cv.split(frame)
    rFilter, gFilter, bFilter = color
    r = r * (rFilter / 255)
    g = g * (gFilter / 255)
    b = b * (bFilter / 255)
    
    frame = cv.merge((b.astype(np.uint8), g.astype(np.uint8), r.astype(np.uint8)))

    return frame

def ascii_to_colored_image(ascii_frame, color_frame):
    height, width = len(ascii_frame), len(ascii_frame[0])
    colored_frame = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            colored_frame[i][j] = color_frame[i][j]
    return colored_frame



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

def endEntryFocus(event):
    if endEntry.get() == '00:00:00':
        endEntry.delete(0, END)
        endEntry.insert(0, '')
        endEntry.config(fg='black')

def endEntryUnfocus(event):
    if endEntry.get() == '':
        endEntry.insert(0, '00:00:00')
        endEntry.config(fg='grey')


def sizeEntryFocus(event):
    if sizeEntry.get() == '0.08':
        sizeEntry.delete(0, END)
        sizeEntry.insert(0, '')
        sizeEntry.config(fg='black')

def sizeEntryUnfocus(event):
    if sizeEntry.get() == '':
        sizeEntry.insert(0, '0.08')
        sizeEntry.config(fg='grey')


def tagEntryFocus(event):
    if tagEntry.get() == '1':
        tagEntry.delete(0, END)
        tagEntry.insert(0, '')
        tagEntry.config(fg='black')

def tagEntryUnfocus(event):
    if tagEntry.get() == '':
        cssText.config(state='normal')
        htmlText.config(state='normal')
        jsText.config(state='normal')
        tagEntry.insert(0, '1')
        htmlText.delete(0, END)
        htmlText.insert(0, f"<canvas id=\"asciianimation"+tagEntry.get()+"\"></canvas>\n<script src=\"asciianimation"+tagEntry.get()+".js\"></script>")
        cssText.delete(0, END)
        cssText.insert(0, f".asciianimation"+tagEntry.get()+"{\n    margin-right: auto;\n    margin-left: auto;\n    align-items: center;\n    padding-right: 0;\n    padding-left: 0;\n}")
        jsText.delete(0,END)
        jsText.insert(0,f"Copy "+".asciianimation"+tagEntry.get()+".js output to desired path")
        tagEntry.config(fg='grey')
        htmlText.config(state='readonly')
        cssText.config(state='readonly')
    else:
        htmlText.config(state='normal')
        cssText.config(state='normal')
        jsText.config(state='normal')
        htmlText.delete(0, END)
        htmlText.insert(0, f"<canvas id=\"asciianimation"+tagEntry.get()+"\"></canvas>\n<script src=\"asciianimation"+tagEntry.get()+".js\"></script>")
        cssText.delete(0, END)
        cssText.insert(0, f".asciianimation"+tagEntry.get()+"{\n    margin-right: auto;\n    margin-left: auto;\n    align-items: center;\n    padding-right: 0;\n    padding-left: 0;\n}")
        jsText.delete(0,END)
        jsText.insert(0,f"Copy "+".asciianimation"+tagEntry.get()+".js output to desired path")

        htmlText.config(state='readonly')
        cssText.config(state='readonly')





def main():
    userVideoInput = selectedFileEntry.get()
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
    factorX = float(sizeEntry.get()) #change to user inputs 
    factorY = float(sizeEntry.get()) #change to user inputs 

    print(factorX)
    print(factorY)

    jsoutput = open("asciianimation"+tagEntry.get()+".js","w")  #clearing javascript file
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

    if endTime != "00:00:00": #user has changed the default, requesting a cut
        endSeconds = int(endTime[0:2]) * 3600 + int(endTime[3:5]) * 60 + int(endTime[6:8])
    else:
        endSeconds = int(cap.get(cv.CAP_PROP_FRAME_COUNT) / fps)

    while cap.isOpened():
        ret, frame = cap.read() #gets next frame
        if not ret or count / fps >= endSeconds:
            print("Done.")
            break
        
        if count / fps >= startSeconds:
            if colorFilterEnabled.get():
                frame = applyColorFilter(frame, userCustomColor)
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
        cv.imshow('resized', frame) #preview
        if cv.waitKey(1) == ord('q'):
            break

    jsoutput = open("asciianimation"+tagEntry.get()+".js","a")

    jsoutput.write("colorValues"+ tagEntry.get() +" ="+str(colorFrames)+";\n")
    jsoutput.write("asciiValues"+ tagEntry.get() +" ="+str(asciiFrames)+";\n")
    jsoutput.write("const canvas"+ tagEntry.get() +" = document.getElementById(\"asciianimation"+ tagEntry.get() +"\");\n")
    jsoutput.write("const ctx"+ tagEntry.get() +" = canvas"+ tagEntry.get() +".getContext(\"2d\");\n")
    jsoutput.write("canvas"+ tagEntry.get() +".width = asciiValues"+ tagEntry.get() +"[0][0].length*8;\n")
    jsoutput.write("canvas"+ tagEntry.get() +".height = asciiValues"+ tagEntry.get() +"[0].length*8;\n")
    jsoutput.write("var frameIndex"+ tagEntry.get() +" = 0;\n")
    jsoutput.write("var interval = window.setInterval(function(){\n")
    jsoutput.write("frameIndex"+ tagEntry.get() +" += 1;\n")
    jsoutput.write("ctx"+ tagEntry.get() +".clearRect(0, 0, canvas"+ tagEntry.get() +".width, canvas"+ tagEntry.get() +".height);\n")
    jsoutput.write("for(let i = 0; i < "+str(windowH)+"; i++){\n")
    jsoutput.write("    for(let j = 0; j < "+str(windowW)+"; j++){\n")
    jsoutput.write("        ctx"+ tagEntry.get() +".font = \"12px "+dropFont.get()[:-4]+", monospace\";\n")
    jsoutput.write("        ctx"+ tagEntry.get() +".fillStyle = \"rgb(\"+String(colorValues"+ tagEntry.get() +"[frameIndex"+ tagEntry.get() +"][i][j][2])+\",\"+String(colorValues"+ tagEntry.get() +"[frameIndex"+ tagEntry.get() +"][i][j][1])+\",\"+String(colorValues"+ tagEntry.get() +"[frameIndex"+ tagEntry.get() +"][i][j][0])+\")\";\n")
    jsoutput.write("        ctx"+ tagEntry.get() +".fillText(asciiValues"+ tagEntry.get() +"[frameIndex"+ tagEntry.get() +"][i][j],j*8,i*8); // might need to change starting location here\n") 
    jsoutput.write("    }\n")
    jsoutput.write("}\n")
    jsoutput.write("if(frameIndex"+ tagEntry.get() +" == "+str(endSeconds*int(fps))+"){\n")
    jsoutput.write("    frameIndex"+ tagEntry.get() +" = 0;\n")
    jsoutput.write("}\n")
    jsoutput.write("}, " + str(int((1000/fps)/ float(dropSpeed.get()))) + " );\n")
    jsoutput.close()
    cap.release()
    cv.destroyAllWindows()
    


    if gifEnabled.get():

        
        if float(dropSpeed.get()) == 0.5:
            gif = imageio.get_writer("output.gif", fps=fps/2, loop=0)
        else:
            gif = imageio.get_writer("output.gif", fps=fps, loop=0)
        for frame_index in range(len(asciiFrames)):
            if frame_index % math.ceil(float(dropSpeed.get())) == 0: 
                canvas_width = len(asciiFrames[0][0]) * 10  # Width of ASCII frame characters
                canvas_height = len(asciiFrames[0]) * 10   # Height of ASCII frame characters
                gifCanvas = PILimg.new('RGB', (canvas_width, canvas_height), color='black')
                gifAsciiColor = ImageDraw.Draw(gifCanvas)
                for i in range(len(asciiFrames[frame_index])):
                    for j in range(len(asciiFrames[frame_index][i])):
                        color = tuple((colorFrames[frame_index][i][j][2], colorFrames[frame_index][i][j][1], colorFrames[frame_index][i][j][0]))
                        
                        font = ImageFont.truetype("./Fonts/" + str(dropFont.get()))
                        gifAsciiColor.text((j * 10, i * 10), asciiFrames[frame_index][i][j], fill=color, font = font) #adjust this based on gif output

                # Append frame to GIF
                gif.append_data(np.array(gifCanvas))
                print("Writing frame:", frame_index)

        gif.close()


    #finished converting .gif and javascript




#do GUI stuff after color
root = Tk()
root.iconbitmap("favicon.ico")
root.title("Javascript Ascii Animation Converter")
root.geometry("460x205")
root.resizable(False, False)

frm = ttk.Frame(root, padding=2.5)
frm.grid()


ttk.Button(frm, text="Browse", command=chooseFile, width=7).grid(column=1, row=1, sticky="w")
selectedFileEntry = ttk.Entry(frm, width=55)
selectedFileEntry.grid(column=0, row=1)

startEntry = Entry(frm, width=7,fg='grey')
startEntry.insert(0, '00:00:00')
startEntry.bind('<FocusIn>', startEntryFocus)
startEntry.bind('<FocusOut>', startEntryUnfocus)
startEntry.grid(column=1, row=3,sticky="w")


startLabel = Label(frm, text="Start")
startLabel.grid(column=1, row=2 ,sticky="w")

endEntry = Entry(frm, width=7,fg='grey')
endEntry.insert(0, '00:00:00')
endEntry.bind('<FocusIn>', endEntryFocus)
endEntry.bind('<FocusOut>', endEntryUnfocus)
endEntry.grid(column=2, row=3, sticky="e")

endLabel = Label(frm, text="End")
endLabel.grid(column=2, row=2, sticky="e")

selectedColorButton = Button(frm, text="Color\nFilter", command=chooseColor, bg = "#ffffff", width=4)
selectedColorButton.grid(column=2, row=8, sticky="e",padx=(28,0), pady=(4,0))

tagEntry = Entry(frm, width=7,fg='grey')
tagEntry.insert(0, '1')
tagEntry.bind('<FocusIn>', tagEntryFocus)
tagEntry.bind('<FocusOut>', tagEntryUnfocus)
tagEntry.grid(column=2, row=7,sticky="e")

tagLabel = Label(frm, text="Tag/ID")
tagLabel.grid(column=2, row=6, sticky="e")






speedLabel = Label(frm, text="Speed")
speedLabel.grid(column=1, row=6, sticky="w")
speed = StringVar(frm)
speed.set("1")
dropSpeed = ttk.Combobox(frm, width = 4, textvariable = speed)
dropSpeed['values'] = [0.5,1,2]
dropSpeed.grid(column=1,row=7,sticky="w")

sizeEntry = Entry(frm, width=7,fg='grey')
sizeEntry.insert(0, '0.08')
sizeEntry.bind('<FocusIn>', sizeEntryFocus)
sizeEntry.bind('<FocusOut>', sizeEntryUnfocus)
sizeEntry.grid(column=2, row=5,sticky="e")

sizeLabel = Label(frm, text="Scale")
sizeLabel.grid(column=2, row=4, sticky="e")


fontVariable = StringVar(frm)
fontVariable.set("Arial.ttf")
dropFont = ttk.Combobox(frm, width = 4, textvariable = fontVariable)
dropFont['values'] = os.listdir("./Fonts/") # get custom fonts
dropFont.grid(column=1,row=5,sticky="w")





fontLabel = Label(frm, text="Font")
fontLabel.grid(column=1, row=4, sticky="w")




#use colorFilterEnabled.get() to see if checked or unchecked
colorFilterEnabled = BooleanVar()
colorFilterCheckbox = Checkbutton(frm, variable=colorFilterEnabled)
colorFilterCheckbox.grid(column=2, row=8, sticky="w")

gifEnabled = BooleanVar()
gifCheckbox = Checkbutton(frm, text=".gif", variable=gifEnabled)
gifCheckbox.grid(column=1, row=8, sticky="w")


ttk.Button(frm, text="Convert", command=main,width=9).grid(column=2, row=1)






selectedFileEntry = Entry(frm, width=55, fg='grey')
selectedFileEntry.insert(0, 'Enter file path or paste YouTube link here')
selectedFileEntry.bind('<FocusIn>', selectedFileEntryFocus)
selectedFileEntry.bind('<FocusOut>', selectedFileEntryUnfocus)
selectedFileEntry.grid(column=0, row=1)

htmlLabel = Label(frm, text="HTML")
htmlLabel.grid(column=0, row=2 ,sticky="w")

htmlText = ttk.Entry(frm, width=50)
htmlText.grid(column=0, row=3)
htmlText.config(state='normal')
htmlText.insert(0,"<canvas id=\"asciianimation"+ tagEntry.get() +"\"></canvas>\n<script src=\"asciianimation"+tagEntry.get()+".js\"></script>")
htmlText.config(state='readonly')

cssLabel = Label(frm, text="CSS")
cssLabel.grid(column=0, row=4 ,sticky="w")

cssText = ttk.Entry(frm, width=50)
cssText.grid(column=0, row= 5)
cssText.config(state='normal')
cssText.insert(0,".asciianimation"+ tagEntry.get() +"{\n    margin-right: auto;\n    margin-left: auto;\n    align-items: center;\n    padding-right: 0;\n    padding-left: 0;\n}")
cssText.config(state='readonly')

jsLabel = Label(frm, text="JS")
jsLabel.grid(column=0, row=6 ,sticky="w")

jsText = ttk.Entry(frm, width=50)
jsText.config(state='normal')
jsText.insert(0,"Copy "+".asciianimation"+tagEntry.get()+".js output to desired path")
jsText.config(state='readonly')
jsText.grid(column=0, row=7)



progressBar = ttk.Progressbar(frm, orient='horizontal', length=200, mode='determinate', maximum=100)
progressBar.grid(row=8, column=0, sticky=E+W+N+S, padx=5, pady=5)

progressLabel = Label(frm, text="Progress: 0%")
progressLabel.place(in_=progressBar, relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()

