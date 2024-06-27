
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
from tkinter import *
import tkinter.ttk as ttk
from bulk import Bulk
from credential import Setup
from volume import Volume

LARGE_FONT = ("Verdana", 12)


class Home(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        self.minsize(500, 120)
        self.menubar = Menu(container)
        self.config(menu=self.menubar)
        self.title("LIQUIDITY CONTROL")
        self.fileMenu = Menu(self.menubar)
        self.fileMenu.add_command(
            label="Configuration", command=lambda: self.show_frame(Setup, container))
        self.menubar.add_cascade(label="Setup", menu=self.fileMenu)
        self.hisMenu = Menu(self.menubar)
        self.hisMenu.add_command(
            label="Add Bulk Order", command=lambda: self.show_frame(Bulk, container))
        self.hisMenu.add_command(
            label="Create Volume", command=lambda: self.show_frame(Volume, container))
        self.menubar.add_cascade(label="Features", menu=self.hisMenu)
        self.exit = Menu(self.menubar)
        self.exit.add_command(label="FAQ", command=lambda: self.quit())
        self.menubar.add_cascade(label="Help", menu=self.exit)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.recycle(container)
        self.show_frame(Volume, container)

    def show_frame(self, cont, container):
        self.recycle(container)
        frame = self.frames[cont]
        container.pack(side="top", fill="both", expand=True)
        frame.tkraise()

    def recycle(self, container):
        for F in (Bulk, Volume, Setup):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")


app = Home()
app.mainloop()
