import numpy as np
import cv2
from tkinter import *
from PIL import Image, ImageTk

#Set up GUI
window = Tk()  #Makes main window
window.wm_title("Digital Microscope")
window.config(background="#FFFFFF")

b = Button(width = 10, height = 2, text = 'Button1')
b.grid(row = 1, column = 0)
b2 = Button(width = 10, height = 2, text = 'Button2')
b2.grid(row = 1,column = 1)

#Slider window (slider controls stage position)
sliderFrame = Frame(window, width=600, height=100)
sliderFrame.grid(row = 600, column=0, padx=10, pady=2)

#Graphics window
imageFrame = Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames
lmain = Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture('http://192.168.0.4:8088/video')
def show_frame():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


show_frame()  #Display 2
window.mainloop()  #Starts GUI