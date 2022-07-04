from locale import currency
from tkinter import *
import tkinter.ttk as ttk
import json
import threading

from utils.exchange import exchangeOrder


class Bulk(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        currency = "USDT"
        try:
            with open('credential.txt') as f:
                lines = f.readlines()
                exchange = lines[0].replace("\n", "")
                if(exchange == '3'):
                    currency = "IDR"
        except:
            currency = "USDT"
        master = Frame(self)
        master.pack(fill=BOTH, expand=True)
        self.par = master
        self.judul = Label(master, text="ADD BULK ORDER",
                           font="Helvetica 16 bold")
        self.judul.grid(row=0, column=0, columnspan=2, ipady=15)

        self._separator = ttk.Separator(master, orient="horizontal")
        self._separator.grid(row=1, column=0, columnspan=2, sticky="we")

        self.label1 = Label(master, text="Budget "+currency+":", pady=3)
        self.label1.grid(row=2, column=0, ipadx=20, sticky=E)
        self.amount = Entry(master)
        self.amount.grid(row=2, column=1, ipadx=20)

        self.label2 = Label(master, text="Start price  : ", pady=3)
        self.label2.grid(row=3, column=0, ipadx=20, sticky=E)
        self.order_start_price = Entry(master)
        self.order_start_price.grid(row=3, column=1, ipadx=20)

        self.label3 = Label(master, text="Trailing Percentage (%) : ", pady=3)
        self.label3.grid(row=4, column=0, ipadx=20, sticky=E)
        self.trailing_percentage = Entry(master)
        self.trailing_percentage.grid(row=4, column=1, ipadx=20)

        self.label4 = Label(master, text="Order Quantity : ", pady=3)
        self.label4.grid(row=5, column=0, ipadx=20, sticky=E)
        self.order_quantity = Entry(master)
        self.order_quantity.grid(row=5, column=1, ipadx=20)

        self.label7 = Label(master, text="Order type : ", pady=3)
        self.label7.grid(row=8, column=0, ipadx=20, sticky=E)
        self.order_type = IntVar()
        frame = Frame(master)
        Radiobutton(frame, text="Sell", variable=self.order_type,
                    value=1).pack(side=RIGHT)
        Radiobutton(frame, text="Buy", variable=self.order_type,
                    value=2).pack(side=RIGHT)
        frame.grid(row=8, column=1, sticky=W)

        self.proses = Button(master, text="PROSES", command=lambda: threading.Thread(
            target=self.processBulkOrder()).start())
        self.proses.grid(row=10, column=0, columnspan=2, pady=10)

        self._separator = ttk.Separator(master, orient="horizontal")
        self._separator.grid(row=11, column=0, columnspan=2, sticky="we")

        self.result = Label(master, text="-", pady=3)
        self.result.grid(row=12, column=0, columnspan=2, sticky="we")

        self._separator = ttk.Separator(master, orient="horizontal")
        self._separator.grid(row=13, column=0, columnspan=2, sticky="we")

        self.res1 = Label(self.par, text=currency+" Per Order : ", pady=3)
        self.res1.grid(row=14, column=0, ipadx=20, sticky=E)
        self.res2 = Label(self.par, text="")
        self.res2.grid(row=14, column=1, ipadx=20, sticky=W)

        self.res3 = Label(self.par, text="Distance per Order : ", pady=3)
        self.res3.grid(row=15, column=0, ipadx=20, sticky=E)
        self.res4 = Label(self.par, text="")
        self.res4.grid(row=15, column=1, ipadx=20, sticky=W)

        self.orderl = Label(self.par, text="Total Order : ", pady=3)
        self.orderl.grid(row=16, column=0, ipadx=20, sticky=E)
        self.order = Label(self.par, text="")
        self.order.grid(row=16, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Success : ", pady=3)
        self.resultl.grid(row=17, column=0, ipadx=20, sticky=E)
        self.success = Label(self.par, text="")
        self.success.grid(row=17, column=1, ipadx=20, sticky=W)

        self.proses = Button(master, text="Show Log", command=self.open_win)
        self.proses.grid(row=19, column=0, columnspan=2, pady=10)

    def processBulkOrder(self):
        valid = self.validation()
        if valid:
            self.result['text'] = "Processing"
            amount = self.amount.get()
            order_start_price = self.order_start_price.get()
            trailing_percentage = self.trailing_percentage.get()
            order_quantity = self.order_quantity.get()
            order_type = self.order_type.get()
            usdt_per_order = float(amount) / int(order_quantity)
            self.res2['text'] = str(usdt_per_order)
            distance_percentage_per_order = float(
                trailing_percentage) / int(order_quantity)
            self.res4['text'] = str(distance_percentage_per_order)
            direction_amplifier = -1 if (int(order_type) == 2) else 1
            if order_type == 2:
                order_type = "buy"
            else:
                order_type = "sell"
            list = []

            self.f = open('log.txt', 'w')
            self.f.write("------DATA------")
            for index in range(int(order_quantity)):
                current_percentage = float(
                    index * distance_percentage_per_order * direction_amplifier)
                price = float(order_start_price) + \
                    float(order_start_price) * current_percentage / 100
                price = round(price, int(self.price_decimals))
                token_per_order = round(
                    float(usdt_per_order / price), int(self.quantity_decimals))
                orderdata = ({"symbol": self.market, "type": order_type,
                              "price": price, "amount": token_per_order, "custom_id": ''})
                self.f.write("\n")
                self.f.write(str(orderdata))
                list.append(orderdata)

            data = json.dumps(list)
            self.order['text'] = str(len(list))
            if self.exchange != "2":
                self.memo = ""
            exchangeOrder(data=data, api_key=self.api_key, private_key=self.private_key,
                          acton="add_bulk_order", exchange=self.exchange, priority=2, memo=self.memo, self=self)

    def validation(self):
        self.result['text'] = "-"
        amount = self.amount.get()
        order_start_price = self.order_start_price.get()
        trailing_percentage = self.trailing_percentage.get()
        order_quantity = self.order_quantity.get()
        order_type = self.order_type.get()
        if amount == "" or order_start_price == "" or trailing_percentage == "" or order_quantity == "" or order_type == 0:
            self.result['text'] = "Field cannot be empty"
            return False
        else:
            try:
                amount = float(self.amount.get())
                order_start_price = float(self.order_start_price.get())
                trailing_percentage = float(self.trailing_percentage.get())
                order_quantity = int(self.order_quantity.get())
                order_type = int(self.order_type.get())
                try:
                    with open('credential.txt') as f:
                        lines = f.readlines()
                        self.exchange = lines[0].replace("\n", "")
                        self.api_key = lines[1].replace("\n", "")
                        self.private_key = lines[2].replace("\n", "")
                        self.market = lines[3].replace("\n", "")
                        self.price_decimals = lines[4].replace("\n", "")
                        self.quantity_decimals = lines[5].replace("\n", "")
                        if self.exchange == "2":
                            self.memo = lines[6].replace("\n", "")
                        return True
                except:
                    self.result['text'] = "Please set your configuration first"
                    return False
            except:
                self.result['text'] = "Field value not valid"
                return False

    def open_win(self):

        new = Toplevel(self)
        new.title("Log ")
        f = open("log.txt")
        t = Text(new, wrap=NONE)
        t.insert(END, str(f.read()))
        t.pack()
