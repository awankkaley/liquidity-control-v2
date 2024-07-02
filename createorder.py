from asyncio import sleep
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox
from tkinter import *
import tkinter.ttk as ttk
import threading
import json
from exchange.exchange import get_trading_depth, exchangeOrder, balance, price, cancel
from exchange.math_utils import random_float
from datetime import datetime
from pysondb import db


class Order(Frame):

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
                api_key_b = lines[7].replace("\n", "")
                private_key_b = lines[8].replace("\n", "")
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
        self.judul = Label(master, text="CREATE ORDER", font="Helvetica 16 bold")
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

        self.label3 = Label(master, text="Expire Time (Seconds) : ", pady=3)
        self.label3.grid(row=4, column=0, ipadx=20, sticky=E)
        self.expire_time = Entry(master)
        self.expire_time.grid(row=4, column=1, ipadx=20)

        self.label6 = Label(master, text="Buy limit percentage (%): : ", pady=3)
        self.label6.grid(row=7, column=0, ipadx=20, sticky=E)
        self.buy_limit_percentage = Entry(master)
        self.buy_limit_percentage.grid(row=7, column=1, ipadx=20)

        self.label7 = Label(master, text="Sell limit percentage (%): : ", pady=3)
        self.label7.grid(row=8, column=0, ipadx=20, sticky=E)
        self.sell_limit_percentage = Entry(master)
        self.sell_limit_percentage.grid(row=8, column=1, ipadx=20)

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

        self.resultl = Label(self.par, text="Quantity : ", pady=3)
        self.resultl.grid(row=18, column=0, ipadx=20, sticky=E)
        self.qty = Label(self.par, text="")
        self.qty.grid(row=18, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Quantity Token Buy: ", pady=3)
        self.resultl.grid(row=19, column=0, ipadx=20, sticky=E)
        self.qty_token_buy = Label(self.par, text="")
        self.qty_token_buy.grid(row=19, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Quantity Token Sell: ", pady=3)
        self.resultl.grid(row=20, column=0, ipadx=20, sticky=E)
        self.qty_token_sell = Label(self.par, text="")
        self.qty_token_sell.grid(row=20, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Order Price Buy: ", pady=3)
        self.resultl.grid(row=21, column=0, ipadx=20, sticky=E)
        self.prb = Label(self.par, text="")
        self.prb.grid(row=21, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Order Price Sell: ", pady=3)
        self.resultl.grid(row=22, column=0, ipadx=20, sticky=E)
        self.prs = Label(self.par, text="")
        self.prs.grid(row=22, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Executed : ", pady=3)
        self.resultl.grid(row=23, column=0, ipadx=20, sticky=E)
        self.ttl = Label(self.par, text="0")
        self.ttl.grid(row=23, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Order Buy : ", pady=3)
        self.resultl.grid(row=24, column=0, ipadx=20, sticky=E)
        self.ob = Label(self.par, text="")
        self.ob.grid(row=24, column=1, ipadx=20, sticky=W)

        self.resultl = Label(self.par, text="Order Sell : ", pady=3)
        self.resultl.grid(row=25, column=0, ipadx=20, sticky=E)
        self.os = Label(self.par, text="")
        self.os.grid(row=25, column=1, ipadx=20, sticky=W)

        self.proses = Button(master, text="Show Log", command=self.open_win)
        self.proses.grid(row=26, column=0, columnspan=2, pady=10)
        try:
            if exchange == "7":
                resA = balance(pair, api_key, private_key, exchange)
                resB = balance(pair, api_key_b, private_key_b, exchange)
                self.tokenA["text"] = resA[0]
                self.tokenB["text"] = resB[1]
            else:
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
        database = db.getDb("db.json")
        exist_data = database.getAll()
        for data in exist_data:
            database.deleteById(data["id"])
        self.active = True
        min_usdt = self.min_usdt.get()
        max_usdt = self.max_usdt.get()
        expire_time = self.expire_time.get()
        buy_limit_percentage = self.buy_limit_percentage.get()
        sell_limit_percentage = self.sell_limit_percentage.get()
        if self.validation() == True:
            self.result["text"] = "Running....."
            self.count = 1
            self.start(
                database,
                float(min_usdt),
                float(max_usdt),
                int(expire_time),
                int(buy_limit_percentage),
                int(sell_limit_percentage),
                self.market,
                int(self.quantity_decimals),
                int(self.price_decimals),
                str(self.api_key),
                str(self.private_key),
                str(getattr(self, 'api_key_b', '')),
                str(getattr(self, 'private_key_b', '')),
                str(self.exchange),
            )

    def validation(self):
        self.result["text"] = "-"
        min_usdt = self.min_usdt.get()
        max_usdt = self.max_usdt.get()
        expire_time = self.expire_time.get()
        buy_limit_percentage = self.buy_limit_percentage.get()
        sell_limit_percentage = self.sell_limit_percentage.get()
        if (
            min_usdt == ""
            or max_usdt == ""
            or expire_time == ""
            or buy_limit_percentage == ""
            or sell_limit_percentage == ""
        ):
            self.result["text"] = "Field cannot be empty"
            return False
        else:
            try:
                min_usdt = float(self.min_usdt.get())
                max_usdt = float(self.max_usdt.get())
                expire_time = int(self.expire_time.get())
                buy_limit_percentage = int(self.buy_limit_percentage.get())
                sell_limit_percentage = int(self.sell_limit_percentage.get())
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
                        if self.exchange == "7":
                            self.api_key_b = lines[7].replace("\n", "")
                            self.private_key_b = lines[8].replace("\n", "")
                        return True
                except:
                    self.result["text"] = "Please set your configuration first"
                    return False
            except:
                self.result["text"] = "Field not valid"
                return False

    def start(
        self,
        database,
        min_usdt,
        max_usdt,
        expire_time,
        buy_limit_percentage,
        sell_limit_percentage,
        market,
        quantity_decimals,
        price_decimals,
        api_key,
        private_key,
        api_key_b,
        private_key_b,
        exchange,
    ):
        delay = expire_time
        thread = threading.Timer(
            delay,
            self.start,
            (
                database,
                min_usdt,
                max_usdt,
                expire_time,
                buy_limit_percentage,
                sell_limit_percentage,
                market,
                quantity_decimals,
                price_decimals,
                api_key,
                private_key,
                api_key_b,
                private_key_b,
                exchange,
            ),
        )
        if self.active == True:
            thread.start()
        if self.exchange != "2":
            self.memo = ""
        self.f = open("log-v.txt", "a")
        count = int(self.ttl["text"]) + 1
        self.ttl["text"] = str(count)

        random_quantity = random_float(min_usdt, max_usdt, quantity_decimals)
        self.qty["text"] = str(random_quantity) + " " + self.currency
        current_price = price(market, exchange)
        buy_price = round(
            current_price - current_price * buy_limit_percentage / 100, price_decimals
        )
        sell_price = round(
            current_price + current_price * sell_limit_percentage / 100, price_decimals
        )
        token_per_order_buy = round(
            float(random_quantity / buy_price), int(quantity_decimals)
        )

        token_per_order_sell = round(
            float(random_quantity / sell_price), int(quantity_decimals)
        )

        self.qty_token_buy["text"] = str(token_per_order_buy)
        self.qty_token_sell["text"] = str(token_per_order_sell)
        self.prb["text"] = str(buy_price) + " " + self.currency
        self.prs["text"] = str(sell_price) + " " + self.currency
        list = []
        list.append(
            {
                "symbol": market,
                "type": "buy",
                "price": buy_price,
                "amount": token_per_order_buy,
                "custom_id": "",
            }
        )
        list.append(
            {
                "symbol": market,
                "type": "sell",
                "price": sell_price,
                "amount": token_per_order_sell,
                "custom_id": "",
            }
        )
        exist_data = database.getAll()
        if len(exist_data) > 0:
            for data in exist_data:
                if exchange == "7":
                    if data["type"] == "sell":
                        cancel(
                            market,
                            data["order_id"],
                            data["type"],
                            api_key,
                            private_key,
                            exchange,
                        )
                    else:
                        cancel(
                            market,
                            data["order_id"],
                            data["type"],
                            api_key_b,
                            private_key_b,
                            exchange,
                        )
                else:
                    cancel(
                        market,
                        data["order_id"],
                        data["type"],
                        api_key,
                        private_key,
                        exchange,
                    )
                database.deleteById(data["id"])

        for item in list:
            try:
                if exchange == "7":
                    if item["type"] == "sell":
                        res = exchangeOrder(
                            item["symbol"],
                            item["type"],
                            item["price"],
                            item["amount"],
                            api_key,
                            private_key,
                            exchange,
                        )
                    else:
                        res = exchangeOrder(
                            item["symbol"],
                            item["type"],
                            item["price"],
                            item["amount"],
                            api_key_b,
                            private_key_b,
                            exchange,
                        )
                else:
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
                    database.add(res)
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
                        + datetime.fromtimestamp(res["created_at"]).strftime(
                            "%d/%m/%Y %H:%M:%S"
                        )
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
                        + datetime.fromtimestamp(res["created_at"]).strftime(
                            "%d/%m/%Y %H:%M:%S"
                        )
                    )

                else:
                    if item["type"] == "buy":
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
            if exchange == "7":
                resA = balance(market, api_key, private_key, exchange)
                resB = balance(market, api_key_b, private_key_b, exchange)
                self.tokenA["text"] = resA[0]
                self.tokenB["text"] = resB[1]
            else:
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
