from faulthandler import disable
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
from tkinter import *
import tkinter.ttk as ttk



class Setup(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        master = Frame(self)
        master.pack(fill=BOTH, expand=True)
        self.judul = Label(master, text="SETUP",font="Helvetica 16 bold")
        self.judul.grid(row=0, column=0, columnspan=2, ipady=15)

        self._separator = ttk.Separator(master, orient="horizontal")
        self._separator.grid(row=1, column=0, columnspan=2, sticky="we")

        self.label1 = Label(master, text="Exchange : ", pady=3)
        self.label1.grid(row=3, column=0, ipadx=20, sticky=E)
        self.var = IntVar()
        frame = Frame(master)  
        Radiobutton(frame, text="LBank", variable=self.var, value=1, command=self.on_select).pack(side = LEFT )
        # Radiobutton(frame, text="Bitmart", variable=self.var, value=2, command=self.on_select).pack(side= LEFT )
        Radiobutton(frame, text="Indodax", variable=self.var, value=3, command=self.on_select).pack(side= LEFT )
        Radiobutton(frame, text="MEXC", variable=self.var, value=4, command=self.on_select).pack(side = LEFT )
        Radiobutton(frame, text="Flybit", variable=self.var, value=5, command=self.on_select).pack(side = LEFT )
        Radiobutton(frame, text="Gate.io", variable=self.var, value=6, command=self.on_select).pack(side = LEFT )
        frame.grid(row=3, column=1, sticky=W)

        self.label2 = Label(master, text="API Key  : ", pady=3 )
        self.label2.grid(row=4, column=0, ipadx=20, sticky=E)
        self.api_key = Entry(master)
        self.api_key.grid(row=4, column=1, ipadx=20)

        self.label3 = Label(master, text="Private Key : ", pady=3)
        self.label3.grid(row=5, column=0, ipadx=20, sticky=E)
        self.private_key = Entry(master)
        self.private_key.grid(row=5, column=1, ipadx=20)

        self.label7 = Label(master, text="Memo : ", pady=3)
        self.label7.grid(row=6, column=0, ipadx=20, sticky=E)
        self.memo = Entry(master)
        self.memo.grid(row=6, column=1, ipadx=20)

        self.label4 = Label(master, text="Market Pair : ", pady=3)
        self.label4.grid(row=7, column=0, ipadx=20, sticky=E)
        self.market = Entry(master)
        self.market.grid(row=7, column=1, ipadx=20)

        self.label5 = Label(master, text="Price Decimal : ", pady=3)
        self.label5.grid(row=8, column=0, ipadx=20, sticky=E)
        self.price_decimals = Entry(master)
        self.price_decimals.grid(row=8, column=1, ipadx=20)

        self.label6 = Label(master, text="Qty Decimal : ", pady=3)
        self.label6.grid(row=9, column=0, ipadx=20, sticky=E)
        self.quantity_decimals = Entry(master)
        self.quantity_decimals.grid(row=9, column=1, ipadx=20)


        self.proses = Button(master, text="PROSES",  command=self.save)
        self.proses.grid(row=10, column=0,columnspan=2, pady=10)

        self._separator = ttk.Separator(master, orient="horizontal")
        self._separator.grid(row=11, column=0, columnspan=2, sticky="we")

        self.result = Label(master, text="-", pady=3)
        self.result.grid(row=12, column=0, columnspan=2, sticky="we")

    def on_select(self):
        if self.var.get() != 2:
            self.label7.grid_forget()
            self.memo.grid_forget()
        else:
            self.label7.grid(row=6, column=0, ipadx=20, sticky=E)
            self.memo.grid(row=6, column=1, ipadx=20)





    def save(self):
        if (self.memo.get() == "" and self.var.get() == 2) or self.api_key.get() == "" or self.private_key.get() == "" or self.market.get() == ""  or self.price_decimals.get() == ""  or self.quantity_decimals.get() == "" or self.var.get() == 0:
            self.result['text'] = "Field cannot be empty"
        else:
            try :
                dat1 = int(self.quantity_decimals.get())
                dat1 = int(self.price_decimals.get())
                with open('credential.txt', 'w') as f:
                    f.write(str(self.var.get()))
                    f.write("\n")
                    f.write(self.api_key.get())
                    f.write("\n")
                    f.write(self.private_key.get())
                    f.write("\n")
                    f.write(self.market.get())
                    f.write("\n")
                    f.write(str(self.price_decimals.get()))
                    f.write("\n")
                    f.write(str(self.quantity_decimals.get()))
                    f.write("\n")
                    f.write(str(self.memo.get()))
                self.result['text'] = "Completed"
            except:
                self.result['text'] = "value not valid"

        

