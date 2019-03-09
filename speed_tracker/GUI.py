from tkinter import *
from PIL import Image
from PIL import ImageTk

import cv2

root = Tk()

canvas = Canvas(root, width=500, height=300, bd = 10, bg = 'white')
canvas.grid(row = 0, column = 0, columnspan = 2)

b = Button(width = 10, height = 2, text = 'Button1')
b.grid(row = 1, column = 0)
b2 = Button(width = 10, height = 2, text = 'Button2')
b2.grid(row = 1,column = 1)

cv2.namedWindow("camera",1)
capture = cv2.VideoCapture('/Users/wfoux200/Desktop/test_file.mkv')

while True:
    image = capture.read()
    im = cv2.imencode(cv2.IMW, image)
    # Rearrang the color channel
    im = Image.fromarray(im)
    im = ImageTk.PhotoImage(im)

    ImageTk.PhotoImage(0,0, image=im)
    if capture.WaitKey(10) == 27:
        break

root.mainloop()