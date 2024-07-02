from asyncio import sleep
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
from tkinter import *
import tkinter.ttk as ttk
import threading
import json
from exchange.exchange import get_trading_depth, exchangeOrder, balance, price
from exchange.math_utils import random_float


class Volume(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        currency = "USDT"
        try:
            with open("credential.txt") as f:
                lines = f.readlines()
                exchange = lines[0].replace("\n", "")
                pair = lines[3].replace("\n", "")
                api_key = lines[1].replace("\n", "")
                private_key = lines[2].replace("\n", "")
                if exchange == "3":
                    currency = lines[3].replace("\n", "").split("_")[1].upper()
                    tokenA = lines[3].replace("\n", "").split("_")[0].upper()
                if exchange == "7":
                    currency = lines[3].replace("\n", "").split("-")[1].upper()
                    tokenA = lines[3].replace("\n", "").split("-")[0].upper()
        except:
            currency = "USDT"
            tokenA = ""

        self.currency = currency
        master = Frame(self)
        master.pack(fill=BOTH, expand=True)
        self.par = master
        self.active = False
        self.judul = Label(master, text="CREATE VOLUME", font="Helvetica 16 bold")
        self.judul.grid(row=0, column=0, columnspan=2, ipady=15)

        self._separator = ttk.Separator(master, orient="horizontal")
        self._separator.grid(row=1, column=0, columnspan=2, sticky="we")

        self.label1 = Label(
            master, text="Random min quantity (" + currency + ") :", pady=3
        )
        self.label1.grid(row=2, column=0, ipadx=20, sticky=E)
        self.min_usdt = Entry(master)
        self.min_usdt.grid(row=2, column=1, ipadx=20)

        self.label2 = Label(
            master, text="Random max quantity (" + currency + ") : ", pady=3
        )
        self.label2.grid(row=3, column=0, ipadx=20, sticky=E)
        self.max_usdt = Entry(master)
        self.max_usdt.grid(row=3, column=1, ipadx=20)

        self.label3 = Label(
            master, text="Min Difference  (" + currency + ") : ", pady=3
        )
        self.label3.grid(row=4, column=0, ipadx=20, sticky=E)
        self.min_price_difference = Entry(master)
        self.min_price_difference.grid(row=4, column=1, ipadx=20)

        self.label4 = Label(master, text="Min Delay in seconds (Ex: 5.5) : ", pady=3)
        self.label4.grid(row=5, column=0, ipadx=20, sticky=E)
        self.delay_min = Entry(master)
        self.delay_min.grid(row=5, column=1, ipadx=20)

        self.label5 = Label(master, text="Max Delay in seconds (Ex: 6.5) : ", pady=3)
        self.label5.grid(row=6, column=0, ipadx=20, sticky=E)
        self.delay_max = Entry(master)
        self.delay_max.grid(row=6, column=1, ipadx=20)

        self.label6 = Label(
            master, text="Maximum limit price (" + currency + "): : ", pady=3
        )
        self.label6.grid(row=7, column=0, ipadx=20, sticky=E)
        self.max_limit_price = Entry(master)
        self.max_limit_price.grid(row=7, column=1, ipadx=20)

        self.label7 = Label(
            master, text="Minimum limit price (" + currency + "): : ", pady=3
        )
        self.label7.grid(row=8, column=0, ipadx=20, sticky=E)
        self.min_limit_price = Entry(master)
        self.min_limit_price.grid(row=8, column=1, ipadx=20)

        self.label8 = Label(master, text="Priority : ", pady=3)
        self.label8.grid(row=10, column=0, ipadx=20, sticky=E)
        self.priority = IntVar()
        frame = Frame(master)
        Radiobutton(frame, text="Mix", variable=self.priority, value=3).pack(side=RIGHT)
        Radiobutton(frame, text="Sell First", variable=self.priority, value=1).pack(
            side=RIGHT
        )
        Radiobutton(frame, text="Buy First", variable=self.priority, value=2).pack(
            side=RIGHT
        )
        frame.grid(row=10, column=1, sticky=W)

        self.proses = Button(
            master,
            text="START",
            command=lambda: threading.Thread(target=self.start_process()).start(),
        )
        self.proses.grid(row=11, column=0, pady=10, sticky=E)

        self.proses = Button(master, text="STOP", command=self.stop)
        self.proses.grid(row=11, column=1, pady=10, sticky=W)

        self._separator = ttk.Separator(master, orient="horizontal")
        self._separator.grid(row=12, column=0, columnspan=2, sticky="we")

        self.result = Label(master, text="-", pady=3)
        self.result.grid(row=13, column=0, columnspan=2, sticky="we")

        self._separator = ttk.Separator(master, orient="horizontal")
        self._separator.grid(row=14, column=0, columnspan=2, sticky="we")

        self.resultl = Label(self.par, text="Balance " + tokenA + " :", pady=3)
        self.resultl.grid(row=15, column=0, ipadx=20, sticky=E)
        self.tokenA = Label(self.par, text="")
        self.tokenA.grid(row=15, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Balance " + currency + " :", pady=3)
        self.resultl.grid(row=16, column=0, ipadx=20, sticky=E)
        self.tokenB = Label(self.par, text="")
        self.tokenB.grid(row=16, column=1, ipadx=20, sticky=W)

        self.curr = Label(self.par, text="Current Price :", pady=3)
        self.curr.grid(row=17, column=0, ipadx=20, sticky=E)
        self.current_price = Label(self.par, text="")
        self.current_price.grid(row=17, column=1, ipadx=20, sticky=W)

        self.res1 = Label(self.par, text="Time : ", pady=3)
        self.res1.grid(row=18, column=0, ipadx=20, sticky=E)
        self.time = Label(self.par, text="")
        self.time.grid(row=18, column=1, ipadx=20, sticky=W)

        self.res1 = Label(self.par, text="Lowest : ", pady=3)
        self.res1.grid(row=19, column=0, ipadx=20, sticky=E)
        self.lowest = Label(self.par, text="")
        self.lowest.grid(row=19, column=1, ipadx=20, sticky=W)

        self.res3 = Label(self.par, text="Highest : ", pady=3)
        self.res3.grid(row=20, column=0, ipadx=20, sticky=E)
        self.highest = Label(self.par, text="")
        self.highest.grid(row=20, column=1, ipadx=20, sticky=W)

        self.orderl = Label(self.par, text="Price Difference: ", pady=3)
        self.orderl.grid(row=21, column=0, ipadx=20, sticky=E)
        self.diff = Label(self.par, text="")
        self.diff.grid(row=21, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Quantity : ", pady=3)
        self.resultl.grid(row=22, column=0, ipadx=20, sticky=E)
        self.qty = Label(self.par, text="")
        self.qty.grid(row=22, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Quantity Token: ", pady=3)
        self.resultl.grid(row=23, column=0, ipadx=20, sticky=E)
        self.qty_token = Label(self.par, text="")
        self.qty_token.grid(row=23, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Order Price : ", pady=3)
        self.resultl.grid(row=24, column=0, ipadx=20, sticky=E)
        self.pr = Label(self.par, text="")
        self.pr.grid(row=24, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Executed : ", pady=3)
        self.resultl.grid(row=25, column=0, ipadx=20, sticky=E)
        self.ttl = Label(self.par, text="0")
        self.ttl.grid(row=25, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Order Buy : ", pady=3)
        self.resultl.grid(row=26, column=0, ipadx=20, sticky=E)
        self.ob = Label(self.par, text="")
        self.ob.grid(row=26, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Order Sell : ", pady=3)
        self.resultl.grid(row=27, column=0, ipadx=20, sticky=E)
        self.os = Label(self.par, text="")
        self.os.grid(row=27, column=1, ipadx=20, sticky=W)

        self.proses = Button(master, text="Show Log", command=self.open_win)
        self.proses.grid(row=28, column=0, columnspan=2, pady=10)
        try:
            res = balance(pair, api_key, private_key, exchange)
            self.tokenA["text"] = res[0]
            self.tokenB["text"] = res[1]
        except Exception as e:
            self.tokenA["text"] = "Failed"
            self.tokenB["text"] = "Failed"
        try:
            res = price(pair, exchange)
            self.current_price["text"] = res
        except Exception as e:
            self.current_price["text"] = "Failed"

    def stop(self):
        self.active = False
        self.result["text"] = "Stoped"

    def start_process(self):
        self.active = True
        min_usdt = self.min_usdt.get()
        max_usdt = self.max_usdt.get()
        min_price_difference = self.min_price_difference.get()
        delay_min = self.delay_min.get()
        delay_max = self.delay_max.get()
        max_limit_price = self.max_limit_price.get()
        min_limit_price = self.min_limit_price.get()
        priority = self.priority.get()
        if self.validation() == True:
            self.result["text"] = "Running....."
            self.count = 1
            self.start(
                delay_min,
                delay_max,
                float(min_price_difference),
                float(min_usdt),
                float(max_usdt),
                float(max_limit_price),
                float(min_limit_price),
                self.market,
                int(self.quantity_decimals),
                int(self.price_decimals),
                str(self.api_key),
                str(self.private_key),
                str(self.exchange),
                int(priority),
            )

    def validation(self):
        self.result["text"] = "-"
        min_usdt = self.min_usdt.get()
        max_usdt = self.max_usdt.get()
        min_price_difference = self.min_price_difference.get()
        delay_min = self.delay_min.get()
        delay_max = self.delay_max.get()
        max_limit_price = self.max_limit_price.get()
        min_limit_price = self.min_limit_price.get()
        priority = self.priority.get()

        if (
            min_usdt == ""
            or max_usdt == ""
            or min_price_difference == ""
            or delay_min == ""
            or delay_max == ""
            or max_limit_price == ""
            or min_limit_price == ""
            or priority == 0
        ):
            self.result["text"] = "Field cannot be empty"
            return False
        else:
            try:
                min_usdt = float(self.min_usdt.get())
                max_usdt = float(self.max_usdt.get())
                min_price_difference = float(self.min_price_difference.get())
                delay_min = float(self.delay_min.get())
                delay_max = float(self.delay_max.get())
                max_limit_price = float(self.max_limit_price.get())
                min_limit_price = float(self.min_limit_price.get())
                priority = int(self.priority.get())
                try:
                    with open("credential.txt") as f:
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
                    self.result["text"] = "Please set your configuration first"
                    return False
            except:
                self.result["text"] = "Field not valid"
                return False

    def start(
        self,
        delay_min,
        delay_max,
        min_price_difference,
        min_usdt,
        max_usdt,
        max_limit_price,
        min_limit_price,
        market,
        quantity_decimals,
        price_decimals,
        api_key,
        private_key,
        exchange,
        priority,
    ):
        delay = random_float(float(delay_min), float(delay_max), 1)
        thread = threading.Timer(
            delay,
            self.start,
            (
                delay_min,
                delay_max,
                min_price_difference,
                min_usdt,
                max_usdt,
                max_limit_price,
                min_limit_price,
                market,
                quantity_decimals,
                price_decimals,
                api_key,
                private_key,
                exchange,
                priority,
            ),
        )
        if self.active == True:
            thread.start()
        if self.exchange != "2":
            self.memo = ""
        self.f = open("log-v.txt", "a")
        trading_depth = get_trading_depth(market, exchange)
        count = int(self.ttl["text"]) + 1
        self.ttl["text"] = str(count)
        lowest_sell = trading_depth[0]
        highest_buy = trading_depth[1]
        self.lowest["text"] = str(lowest_sell)
        self.highest["text"] = str(highest_buy)
        price_difference = round(lowest_sell - highest_buy, price_decimals)
        self.diff["text"] = str(price_difference)
        if (
            min_price_difference <= price_difference
            and highest_buy <= max_limit_price
            and lowest_sell >= min_limit_price
        ):
            random_quantity = random_float(min_usdt, max_usdt, quantity_decimals)
            self.qty["text"] = str(random_quantity) + " " + self.currency
            random_price = random_float(highest_buy, lowest_sell, price_decimals)
            token_per_order = round(
                float(random_quantity / random_price), int(quantity_decimals)
            )
            self.qty_token["text"] = str(token_per_order)
            self.pr["text"] = str(random_price) + " " + self.currency
            list = []
            if priority == 1:
                list.append(
                    {
                        "symbol": market,
                        "type": "sell",
                        "price": random_price,
                        "amount": token_per_order,
                        "custom_id": "",
                    }
                )
                list.append(
                    {
                        "symbol": market,
                        "type": "buy",
                        "price": random_price,
                        "amount": token_per_order,
                        "custom_id": "",
                    }
                )
            if priority == 2:
                list.append(
                    {
                        "symbol": market,
                        "type": "buy",
                        "price": random_price,
                        "amount": token_per_order,
                        "custom_id": "",
                    }
                )
                list.append(
                    {
                        "symbol": market,
                        "type": "sell",
                        "price": random_price,
                        "amount": token_per_order,
                        "custom_id": "",
                    }
                )
            if priority == 3:
                if self.count % 2 == 0:
                    list.append(
                        {
                            "symbol": market,
                            "type": "buy",
                            "price": random_price,
                            "amount": token_per_order,
                            "custom_id": "",
                        }
                    )
                    list.append(
                        {
                            "symbol": market,
                            "type": "sell",
                            "price": random_price,
                            "amount": token_per_order,
                            "custom_id": "",
                        }
                    )
                else:
                    list.append(
                        {
                            "symbol": market,
                            "type": "sell",
                            "price": random_price,
                            "amount": token_per_order,
                            "custom_id": "",
                        }
                    )
                    list.append(
                        {
                            "symbol": market,
                            "type": "buy",
                            "price": random_price,
                            "amount": token_per_order,
                            "custom_id": "",
                        }
                    )
            for item in list:
                if self.active == False:
                    break
                try:
                    res = exchangeOrder(
                        item["symbol"],
                        item["type"],
                        item["price"],
                        item["amount"],
                        api_key,
                        private_key,
                        exchange,
                    )
                    if res["success"] == True:
                        if res["type"] == "buy":
                            self.ob["text"] = "Succes"
                        else:
                            self.os["text"] = "Succes"
                        self.f.write(
                            "Order "
                            + item["type"]
                            + ": Succes"
                            + " ID: "
                            + str(res["order_id"])
                            + " Price: "
                            + str(item["price"])
                            + " Amount: "
                            + str(item["amount"])
                            + " Time: "
                            + res["created_at"].strftime("%d/%m/%Y %H:%M:%S")
                        )
                        self.f.write("\n")
                        print(
                            "Order "
                            + item["type"]
                            + ": Succes"
                            + " ID: "
                            + str(res["order_id"])
                            + " Price: "
                            + str(item["price"])
                            + " Amount: "
                            + str(item["amount"])
                            + " Time: "
                            + res["created_at"].strftime("%d/%m/%Y %H:%M:%S")
                        )
    
                    else:
                        if res["type"] == "buy":
                            self.ob["text"] = str("Failed-" + str(res["errorMessage"]))
                        else:
                            self.os["text"] = str("Failed-" + str(res["errorMessage"]))
                        self.f.write(
                            "Order "
                            + item["type"]
                            + ": Failed-"
                            + "-"
                            + str(res["errorMessage"])
                        )
                        self.f.write("\n")
                        print(
                            "Order  "
                            + item["type"]
                            + ": Failed-"
                            + "-"
                            + str(res["errorMessage"])
                        )
                except Exception as e:
                    print(str(e))
                    if item["type"] == "buy":
                        self.ob["text"] = str("Failed- Request Failed")
                    else:
                        self.os["text"] = str("Failed- Request Failed")
                    self.f.write("Order  " + item["type"] + ": Failed-Request Failed")
                    self.f.write("\n")
                    print("Order  " + item["type"] + ": Failed- Request Failed")
    
                try:
                    res = balance(market, api_key, private_key, exchange)
                    self.tokenA["text"] = res[0]
                    self.tokenB["text"] = res[1]
                except Exception as e:
                    self.tokenA["text"] = "Failed"
                    self.tokenB["text"] = "Failed"
                try:
                    res = price(market, exchange)
                    self.current_price["text"] = res
                except Exception as e:
                    self.current_price["text"] = "Failed"
    
                    self.current_price["text"] = "Failed"
                self.count += 1
            self.f.write("\n")
            self.f.close()

    def open_win(self):
        new = Toplevel(self)
        new.title("Log ")
        f = open("log-v.txt")
        t = Text(new, wrap=NONE)
        t.place
        t.insert(END, str(f.read()))
        t.pack(fill=BOTH, expand=1)
