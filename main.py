# starting point of our project where the GUI and Hugging Face Models will be launched

#importing main gui class from gui.py
from gui import AIApp

if __name__ == "__main__":
    app = AIApp()               #creating an instance

    #starting the tkinter main loop
    app.mainloop()
