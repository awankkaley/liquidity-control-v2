from asyncio import sleep
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
from tkinter import *
import tkinter.ttk as ttk
import threading
import json
from utils.exchange import get_trading_depth, exchangeOrder
from utils.math_utils import random_float


class Volume(Frame):

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
        self.currency = currency
        master = Frame(self)
        master.pack(fill=BOTH, expand=True)
        self.par = master
        self.active = False
        self.judul = Label(master, text="CREATE VOLUME",
                           font="Helvetica 16 bold")
        self.judul.grid(row=0, column=0, columnspan=2, ipady=15)

        self._separator = ttk.Separator(master, orient="horizontal")
        self._separator.grid(row=1, column=0, columnspan=2, sticky="we")

        self.label1 = Label(
            master, text="Random min quantity ("+currency+") :", pady=3)
        self.label1.grid(row=2, column=0, ipadx=20, sticky=E)
        self.min_usdt = Entry(master)
        self.min_usdt.grid(row=2, column=1, ipadx=20)

        self.label2 = Label(
            master, text="Random max quantity ("+currency+") : ", pady=3)
        self.label2.grid(row=3, column=0, ipadx=20, sticky=E)
        self.max_usdt = Entry(master)
        self.max_usdt.grid(row=3, column=1, ipadx=20)

        self.label3 = Label(
            master, text="Min Difference  ("+currency+") : ", pady=3)
        self.label3.grid(row=4, column=0, ipadx=20, sticky=E)
        self.min_price_difference = Entry(master)
        self.min_price_difference.grid(row=4, column=1, ipadx=20)

        self.label4 = Label(
            master, text="Delay in seconds (Ex: 5.5) : ", pady=3)
        self.label4.grid(row=5, column=0, ipadx=20, sticky=E)
        self.delay = Entry(master)
        self.delay.grid(row=5, column=1, ipadx=20)

        self.label5 = Label(
            master, text="Maximum limit price ("+currency+"): : ", pady=3)
        self.label5.grid(row=6, column=0, ipadx=20, sticky=E)
        self.max_limit_price = Entry(master)
        self.max_limit_price.grid(row=6, column=1, ipadx=20)

        self.label6 = Label(
            master, text="Minimum limit price ("+currency+"): : ", pady=3)
        self.label6.grid(row=7, column=0, ipadx=20, sticky=E)
        self.min_limit_price = Entry(master)
        self.min_limit_price.grid(row=7, column=1, ipadx=20)

        self.label7 = Label(master, text="Priority : ", pady=3)
        self.label7.grid(row=8, column=0, ipadx=20, sticky=E)
        self.priority = IntVar()
        frame = Frame(master)
        Radiobutton(frame, text="Mix",
                    variable=self.priority, value=3).pack(side=RIGHT)
        Radiobutton(frame, text="Sell First",
                    variable=self.priority, value=1).pack(side=RIGHT)
        Radiobutton(frame, text="Buy First",
                    variable=self.priority, value=2).pack(side=RIGHT)
        frame.grid(row=8, column=1, sticky=W)

        self.proses = Button(master, text="START", command=lambda: threading.Thread(
            target=self.start_process()).start())
        self.proses.grid(row=10, column=0, pady=10, sticky=E)

        self.proses = Button(master, text="STOP", command=self.stop)
        self.proses.grid(row=10, column=1, pady=10, sticky=W)

        self._separator = ttk.Separator(master, orient="horizontal")
        self._separator.grid(row=11, column=0, columnspan=2, sticky="we")

        self.result = Label(master, text="-", pady=3)
        self.result.grid(row=12, column=0, columnspan=2, sticky="we")

        self._separator = ttk.Separator(master, orient="horizontal")
        self._separator.grid(row=13, column=0, columnspan=2, sticky="we")

        self.res1 = Label(self.par, text="Time : ", pady=3)
        self.res1.grid(row=14, column=0, ipadx=20, sticky=E)
        self.time = Label(self.par, text="")
        self.time.grid(row=14, column=1, ipadx=20, sticky=W)

        self.res1 = Label(self.par, text="Lowest : ", pady=3)
        self.res1.grid(row=15, column=0, ipadx=20, sticky=E)
        self.lowest = Label(self.par, text="")
        self.lowest.grid(row=15, column=1, ipadx=20, sticky=W)

        self.res3 = Label(self.par, text="Highest : ", pady=3)
        self.res3.grid(row=16, column=0, ipadx=20, sticky=E)
        self.highest = Label(self.par, text="")
        self.highest.grid(row=16, column=1, ipadx=20, sticky=W)

        self.orderl = Label(self.par, text="Price Difference: ", pady=3)
        self.orderl.grid(row=17, column=0, ipadx=20, sticky=E)
        self.diff = Label(self.par, text="")
        self.diff.grid(row=17, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Quantity : ", pady=3)
        self.resultl.grid(row=18, column=0, ipadx=20, sticky=E)
        self.qty = Label(self.par, text="")
        self.qty.grid(row=18, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Quantity Token: ", pady=3)
        self.resultl.grid(row=19, column=0, ipadx=20, sticky=E)
        self.qty_token = Label(self.par, text="")
        self.qty_token.grid(row=19, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Price : ", pady=3)
        self.resultl.grid(row=20, column=0, ipadx=20, sticky=E)
        self.pr = Label(self.par, text="")
        self.pr.grid(row=20, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Executed : ", pady=3)
        self.resultl.grid(row=21, column=0, ipadx=20, sticky=E)
        self.ttl = Label(self.par, text="0")
        self.ttl.grid(row=21, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Order Buy : ", pady=3)
        self.resultl.grid(row=22, column=0, ipadx=20, sticky=E)
        self.ob = Label(self.par, text="")
        self.ob.grid(row=22, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Order Sell : ", pady=3)
        self.resultl.grid(row=23, column=0, ipadx=20, sticky=E)
        self.os = Label(self.par, text="")
        self.os.grid(row=23, column=1, ipadx=20, sticky=W)

        self.proses = Button(master, text="Show Log", command=self.open_win)
        self.proses.grid(row=25, column=0, columnspan=2, pady=10)

    def stop(self):
        self.active = False
        self.result['text'] = "Stoped"

    def start_process(self):
        self.active = True
        min_usdt = self.min_usdt.get()
        max_usdt = self.max_usdt.get()
        min_price_difference = self.min_price_difference.get()
        delay = self.delay.get()
        max_limit_price = self.max_limit_price.get()
        min_limit_price = self.min_limit_price.get()
        priority = self.priority.get()
        if self.validation() == True:
            self.result['text'] = "Running....."
            self.count = 1
            self.start(float(delay), float(min_price_difference), float(min_usdt), float(max_usdt), float(max_limit_price), float(min_limit_price), self.market, int(
                self.quantity_decimals), int(self.price_decimals), str(self.api_key), str(self.private_key), str(self.exchange), int(priority))

    def validation(self):
        self.result['text'] = "-"
        min_usdt = self.min_usdt.get()
        max_usdt = self.max_usdt.get()
        min_price_difference = self.min_price_difference.get()
        delay = self.delay.get()
        max_limit_price = self.max_limit_price.get()
        min_limit_price = self.min_limit_price.get()
        priority = self.priority.get()

        if min_usdt == "" or max_usdt == "" or min_price_difference == "" or delay == "" or max_limit_price == "" or min_limit_price == "" or priority == 0:
            self.result['text'] = "Field cannot be empty"
            return False
        else:
            try:
                min_usdt = float(self.min_usdt.get())
                max_usdt = float(self.max_usdt.get())
                min_price_difference = float(self.min_price_difference.get())
                delay = float(self.delay.get())
                max_limit_price = float(self.max_limit_price.get())
                min_limit_price = float(self.min_limit_price.get())
                priority = int(self.priority.get())
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
                self.result['text'] = "Field not valid"
                return False

    def start(self, delay, min_price_difference, min_usdt, max_usdt, max_limit_price, min_limit_price, market, quantity_decimals, price_decimals, api_key, private_key, exchange, priority):
        thread = threading.Timer(delay, self.start, (delay, min_price_difference, min_usdt, max_usdt, max_limit_price,
                                 min_limit_price, market, quantity_decimals, price_decimals, api_key, private_key, exchange, priority))
        if self.active == True:
            thread.start()
        if self.exchange != "2":
            self.memo = ""
        self.f = open('log-v.txt', 'a')
        trading_depth = get_trading_depth(market, exchange)
        count = int(self.ttl['text'])+1
        self.ttl['text'] = str(count)
        lowest_sell = trading_depth[0]
        highest_buy = trading_depth[1]
        print("Lowest : "+str(lowest_sell))
        self.lowest['text'] = str(lowest_sell)
        print("Highest : "+str(highest_buy))
        self.highest['text'] = str(highest_buy)
        price_difference = round(lowest_sell - highest_buy, price_decimals)
        print('Current Price Difference: ' + str(price_difference))
        self.diff['text'] = str(price_difference)
        if min_price_difference <= price_difference and highest_buy <= max_limit_price and lowest_sell >= min_limit_price:
            random_quantity = random_float(
                min_usdt, max_usdt, quantity_decimals)
            print('BuySell Quantity: ' + str(random_quantity) + " "+self.currency)
            self.qty['text'] = str(random_quantity) + " "+self.currency
            random_price = random_float(
                highest_buy, lowest_sell, price_decimals)
            token_per_order = round(
                float(random_quantity / random_price), int(quantity_decimals))
            print('BuySell Quantity Token: ' + str(token_per_order))
            self.qty_token['text'] = str(token_per_order)
            print('BuySell Price: ' + str(random_price) + " "+self.currency)
            self.pr['text'] = str(random_price) + " "+self.currency
            print("COUNT : "+str(self.count))
            list = []
            if priority == 1:
                list.append({"symbol": market, "type": 'sell', "price": random_price,
                            "amount": token_per_order, "custom_id": ''})
                list.append({"symbol": market, "type": 'buy', "price": random_price,
                            "amount": token_per_order, "custom_id": ''})
            if priority == 2:
                list.append({"symbol": market, "type": 'buy', "price": random_price,
                            "amount": token_per_order, "custom_id": ''})
                list.append({"symbol": market, "type": 'sell', "price": random_price,
                            "amount": token_per_order, "custom_id": ''})
            if priority == 3:
                if self.count % 2 == 0:
                    list.append({"symbol": market, "type": 'buy', "price": random_price,
                                "amount": token_per_order, "custom_id": ''})
                    list.append({"symbol": market, "type": 'sell', "price": random_price,
                                "amount": token_per_order, "custom_id": ''})
                else:
                    list.append({"symbol": market, "type": 'sell', "price": random_price,
                                "amount": token_per_order, "custom_id": ''})    
                    list.append({"symbol": market, "type": 'buy', "price": random_price,
                                "amount": token_per_order, "custom_id": ''})                
            data = json.dumps(list)
            self.f.write("Data : " + str(data))
            self.f.write("\n")
            exchangeOrder(data=data, api_key=api_key, private_key=private_key, acton="create_volume",
                          exchange=exchange, priority=priority, memo=self.memo, self=self)
            self.count += 1
        self.f.write("\n")
        self.f.close()

    def open_win(self):
        new = Toplevel(self)
        new.title("Log ")
        f = open("log-v.txt")
        t = Text(new, wrap=NONE)
        t.insert(END, str(f.read()))
        t.pack()
