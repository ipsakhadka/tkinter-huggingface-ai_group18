#importing from tkinter

from tkinter import *

#creating main window

root = Tk()

#creating a Label widget
#first label
myLabel1 = Label(root, text="This is the starting phase for Assignment 3.")

#second label
myLabel2 = Label(root, text="FOR SOFTWARE NOW!")

#placing labels in the window
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=0)

#lets run the application window
root.mainloop()