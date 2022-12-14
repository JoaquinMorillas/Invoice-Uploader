from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
import tkinter.font as tkFont

from frontEnd import Window

WIDTH = 475
HEIGHT = 1200

root = Tk()
win = Window(root, WIDTH, HEIGHT)


win.mainloop()


#TODO agregar messagesbox para la confirmacion y errores, agregar la opcion de borrar una factura(Preguntar)