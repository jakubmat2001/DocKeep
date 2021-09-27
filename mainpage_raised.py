
from tkinter import EXCEPTION, messagebox
from tkinter import ttk, filedialog
from tkinter.constants import END, INSERT
from PIL import ImageTk, Image
from commondata import lotsize_values
import webbrowser
import pickle
import tkinter as tk
import string
import dict_data

# various fonts used for label widgets
App_font = ("Sans-Serif", 13)
Body_font = ("Sans-Serif", 9)

# the main window of application that is going to be displayed upon application launch
class mainpage(tk.Frame):
    def __init__(self, parent, controller):
        import four_hour_raised, one_hour_raised, fifteen_min_raised, result_raised
        tk.Frame.__init__(self, parent)
        
        # variables use to retrive data from multiple application UI forms/boxes
        balance_val = tk.DoubleVar(value=(dict_data.get_dict_data["balance"]))
        slider_val = tk.IntVar()
        slider_entry_box = tk.IntVar()
        ld_radio_val = tk.IntVar()
        bs_radio_val = tk.StringVar()
        tp_var = tk.DoubleVar()
        sl_var = tk.DoubleVar()
        
        # variable used for end result variables
        self.int_lot_size_val = 0
        self.updated_exchange_rate = 0 
        self.position_size = 0

        self.balance = 0
        self.lev_balance = 0.0
        self.result = 0.0

        # These variables will decide if program will continue running or not
        self.validation_check = True
        self.validation_check_2 = True

        self.alert_activation = False
        self.validate_result_check = False
        
        # Buy & Sell radio boxes values
        self.sl_val = sl_var.get()
        self.tp_val = tp_var.get()

        # conversion rates to GBP
        self.usd_to_gbp = 0
        self.euro_to_gbp = 0
        self.aud_to_gbp = 0

        # up-to-date exchange rates 
        self.exchange_gbp_usd = 0
        self.exchange_euro_usd = 0
        self.exchange_aud_usd = 0

        self.bid_exchange_rate = 0.0
        self.ask_exchange_rate = 0.0

        self.buysell_exchange = 0.0
        
        # converts position size into pounds
        self.conversion = 0

        # main page frames
        self.tabs_bar = tk.Frame(self, bg="#DC7979")
        self.tabs_bar.grid(row=0, column=0, sticky="we")

        self.banner_lbl = tk.Label(self, text="Doc Keep Page",font=App_font ,width=120, height=5, bg="#BDBABA")
        self.banner_lbl.grid(row=1, column=0, sticky="we")

        self.main_body = tk.Frame(self, bg="#FDFDFD")
        self.main_body.grid(row=2, column=0, sticky="nsew")

        self.bottom_tab = tk.Frame(self, bg="#DC7979", height=35, width=10)
        self.bottom_tab.grid(row=3, column=0, sticky="we") 
        
        self.radio_buy_sell = tk.Frame(self.main_body, bg="#FDFDFD")
        self.radio_buy_sell.grid(row=4, column=2, rowspan=2, pady=(0,45))
        

        # buttons
        self.button = tk.Button(self.tabs_bar, text="Main" ,command=lambda: controller.show_frame(mainpage), borderwidth=1, relief="solid")
        self.button.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

        self.button2 = tk.Button(self.tabs_bar, text="4 Hour", command=lambda: controller.show_frame(four_hour_raised.four_hour), borderwidth=1, relief="solid")
        self.button2.grid(row=0, column=2, padx=(5, 5), pady=(5, 5))

        self.button3 = tk.Button(self.tabs_bar, text="1 Hour", command=lambda: controller.show_frame(one_hour_raised.one_hour), borderwidth=1, relief="solid")
        self.button3.grid(row=0, column=3, padx=(5, 5), pady=(5, 5))

        self.button4 = tk.Button(self.tabs_bar, text="15 Min", command=lambda: controller.show_frame(fifteen_min_raised.fifteen_min), borderwidth=1, relief="solid")
        self.button4.grid(row=0, column=4, padx=(5, 5), pady=(5, 5))

        self.button5 = tk.Button(self.tabs_bar, text="Result", command=lambda: controller.show_frame(result_raised.result), borderwidth=1, relief="solid")
        self.button5.grid(row=0, column=5, padx=(5, 5), pady=(5, 5))

        # Upper most section of gui / balance modification & light and dark mode
        self.balance_lbl = tk.Label(self.main_body, text="Current Balance:", font=Body_font, bg="#FDFDFD")
        self.balance_lbl.grid(row=0, column=0, padx=(15, 0), pady=(5,0))

        self.text_box = tk.Label(self.main_body, width=10, height=1, text=balance_val.get() , borderwidth=1, relief="sunken", bg="white")
        self.text_box.grid(row=0, column=1, padx=(5, 0), pady=(5,0))

        self.mod_bal_button = ttk.Button(self.main_body, text="Modify Balance", command=lambda:enter_balance(self))
        self.mod_bal_button.grid(row=0, column=2, padx=(15, 0), pady=(8,0))

        self.light_md = ttk.Radiobutton(self.main_body, variable=ld_radio_val ,text="Light Mode", value=1, command=lambda:theme_mode(self, ld_radio_val))
        self.light_md.grid(row=0, column=5, padx=(230,0))
        self.dark_md = ttk.Radiobutton(self.main_body, variable=ld_radio_val ,text="Dark Mode", value=2, command=lambda:theme_mode(self, ld_radio_val))
        self.dark_md.grid(row=0, column=6, padx=(20,0))

        # Mid section of gui / chart buttons, exchange pair, lot-size, update exchange rate, buy & sell positions
        self.exchange_lbl = tk.Label(self.main_body, text="Current Exchange Rate", font=Body_font, bg="#FDFDFD")
        self.exchange_lbl.grid(row=1, column=0, padx=(20, 0), pady=(100,0))

        self.exchange_rate_box = tk.Label(self.main_body, width=8, borderwidth=1, relief="sunken")
        self.exchange_rate_box.grid(row=2, column=0, padx=(10,0), pady=(10,0))

        self.update_exchange_button = ttk.Button(self.main_body, text="       Update\nExchange-Rate", command=lambda:display_exchange_rate(self))
        self.update_exchange_button.grid(row=3, column=0, padx=(10,0), pady=(0,40))

        self.curreny_pair_lbl = tk.Label(self.main_body, text="Now Showing:", font=Body_font,  bg="#FDFDFD")
        self.curreny_pair_lbl.grid(row=1, column=2, padx=(15,0), pady=(100,0))

        self.currency_pair_combo = ttk.Combobox(self.main_body, width=15, state="readonly")
        self.currency_pair_combo['values'] = ("GBP/USD", "GBP/CAD", "AUD/USD", "EURO/USD")
        self.currency_pair_combo.grid(row=2, column=2, padx=(15,0), pady=(10,0))

        self.lot_size_lbl = tk.Label(self.main_body, text="Lot Size:", font=Body_font, bg="#FDFDFD")
        self.lot_size_lbl.grid(row=1, column=3, padx=(20,0), pady=(100,0))

        self.lot_size_box = tk.Entry(self.main_body, width=8, relief="groove", bd=2, textvariable=slider_entry_box)
        self.lot_size_box.grid(row=2, column=3, padx=(20,0), pady=(9,0))

        self.lot_size_scale = ttk.Scale(self.main_body, orient=tk.HORIZONTAL,variable=slider_val ,from_=0, to=10000, length=130, command=lambda x:select_lotsize(self))
        self.lot_size_scale.grid(row=3, column=3, padx=(80,0), pady=(0,80))

        self.upload_charts = ttk.Button(self.main_body, text="Upload\n Charts", command=lambda: upload_all_charts(self))
        self.upload_charts.grid(row=2, column=6, padx=(0, 0), pady=(35, 0))

        #bottom section gui / place trade, close trade, buy & sell positions
        self.place_trade_button = ttk.Button(self.main_body, text="Place\nTrade", command=lambda:place_trade(self), state="disabled")
        self.place_trade_button.grid(row=4, column=0, pady=(20,0))

        self.close_trade_button = ttk.Button(self.main_body, text="Close\nTrade", command=lambda:close_trade(self))
        self.close_trade_button.grid(row=5, column=0, pady=(20,50))

        self.buy_sell_lbl = tk.Label(self.radio_buy_sell, text="Select Position")
        self.buy_sell_lbl.grid(row=3, column=2, pady=(0,0))

        self.buy_radio = ttk.Radiobutton(self.radio_buy_sell, variable=bs_radio_val ,text="Buy", value="buy")
        self.buy_radio.grid(row=4, column=2 , pady=(10,0))

        self.sell_radio = ttk.Radiobutton(self.radio_buy_sell, variable=bs_radio_val , text="Sell", value="sell")
        self.sell_radio.grid(row=5, column=2, pady=(10,0))

        self.tp_label = tk.Label(self.main_body, text="Set TP")
        self.tp_label.grid(row=4 , column=3, pady=(0,10))

        self.tp_box = tk.Entry(self.main_body, width=7, relief="groove", bd=2 , textvariable=tp_var)
        self.tp_box.grid(row=4, column=3, pady=(60,0))

        self.tp_change_button = ttk.Button(self.main_body, text="Modify TP", command=lambda:change_tp(self))
        self.tp_change_button.grid(row=4, column=3, rowspan=3, pady=(30,0))

        self.sl_label = tk.Label(self.main_body, text="Set SL")
        self.sl_label.grid(row=4 , column=4, pady=(0,10))

        self.sl_box = tk.Entry(self.main_body, width=7, relief="groove", bd=2, textvariable=sl_var)
        self.sl_box.grid(row=4, column=4, pady=(60,0))

        self.sl_change_button = ttk.Button(self.main_body, text="Modify SP", command=lambda:change_sl(self))
        self.sl_change_button.grid(row=4, column=4, rowspan=3, pady=(30,0))

        self.guide_lbl = tk.Label(self.main_body, text="Video Guide", font=Body_font, bg="#FDFDFD")
        self.guide_lbl.grid(row=4, column=6)

        self.guide_button = ttk.Button(self.main_body, text="  Video  \nTutorial", command= lambda: yt_link(self) )
        self.guide_button.grid(row=5, column=6, pady=(0, 70))


        # ------------------------------------------- Main Functions ---------------------------------------------- #

        # changes TP after a trade has been placed (can be used only after trade has been placed)
        def change_tp(self):
            try:
                self.sl_val = sl_var.get()
                self.sl_val = float(self.sl_val)
                self.tp_val = tp_var.get()
                self.tp_val = float(self.tp_val)
                str1 = self.tp_box.get()
                try:
                    if self.tp_box.get() == "0.0":
                        dict_data.startup_load_values_to_startup()
                        dict_data.st_values_holder["TP"] = 0.0
                        dict_data.placetrade_values_holder["TP"] = 0.0

                        start_up = open("startup_vars", "wb")
                        pickle.dump(dict_data.st_values_holder, start_up)
                        start_up.close()
                        messagebox.showinfo("TP Reset", "TP has been removed")
                    elif len(self.tp_box.get()) < 7:
                        messagebox.showinfo("TP Invalid Input", "      Please enter valid exchange rate \nExchange rate needs to be 7 characters long")
                        self.tp_box.delete(0, END)
                        self.tp_box.insert(0, "0.0")
                    elif len(self.tp_box.get()) > 7:
                        messagebox.showinfo("TP Invalid Input", "Please enter valid exchange rate \nNo more than 7 characters long")
                        self.tp_box.delete(0, END)
                        self.tp_box.insert(0, "0.0")
                    elif str1[1] != ".":
                        messagebox.showinfo("TP Invalid Input", "Please enter valid exchange rate \nThe entered value needs to be a float\n                     e.g 1.40232")
                        self.tp_box.delete(0, END)
                        self.tp_box.insert(0, "0.0")
                    else:
                        if dict_data.placetrade_values_holder.get("buysell") == "buy" and self.sl_val >= self.tp_val:
                            messagebox.showinfo("Invalid Request TP", "You cannot set (SL > TP)\n  When postion = 'buy'")
                        elif dict_data.placetrade_values_holder.get("buysell") == "sell" and self.tp_val >= self.sl_val:
                            messagebox.showinfo("Invalid Request TP", "You cannot set (TP > SL)\n  When position = 'sell'")
                        elif dict_data.placetrade_values_holder.get("buysell") == "buy" and dict_data.placetrade_values_holder.get("open") >= self.tp_val:
                            messagebox.showinfo("Invalid Request TP", "You cannot set (Open Price > TP)\n     When position = 'buy'")
                        elif dict_data.placetrade_values_holder.get("buysell") == "sell" and self.tp_val >= dict_data.placetrade_values_holder.get("open"):
                            messagebox.showinfo("Invalid Request TP", "You cannot set (TP > Open Price)\n     When postion = 'sell'")
                        else:
                            dict_data.startup_load_values_to_startup()
                            dict_data.st_values_holder["TP"] = round(self.tp_val, 5)
                            dict_data.placetrade_values_holder["TP"] = round(self.tp_val, 5)

                            start_up = open("startup_vars", "wb")
                            pickle.dump(dict_data.st_values_holder, start_up)
                            start_up.close()
                            messagebox.showinfo("TP Changed", "TP has been changed to " + str(self.tp_val))
                except Exception:
                    messagebox.showinfo("TP Error", "Something went wrong" + "\nReseting TP to default values")
                    dict_data.startup_load_values_to_startup()
                    dict_data.st_values_holder["TP"] = 0.0
                    dict_data.placetrade_values_holder["TP"] = 0.0

                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    self.tp_box.delete(0, END)
                    self.tp_box.insert(0, "0.0")
            except Exception:
                messagebox.showinfo("TP Invalid Input", "TP box accepts only numbers")
            
            


        # changes SL after a trade has been placed (can be used only after trade has been placed)
        def change_sl(self):
            try:
                self.sl_val = sl_var.get()
                self.sl_val = float(self.sl_val)
                self.tp_val = tp_var.get()
                self.tp_val = float(self.tp_val)
                str1 = self.sl_box.get()
                try:
                    if self.sl_box.get() == "0.0": 
                        dict_data.startup_load_values_to_startup()
                        dict_data.st_values_holder["SL"] = 0.0
                        dict_data.placetrade_values_holder["SL"] = 0.0

                        start_up = open("startup_vars", "wb")
                        pickle.dump(dict_data.st_values_holder, start_up)
                        start_up.close()
                        messagebox.showinfo("SL Reset", "SL has been removed")
                    elif len(self.sl_box.get()) < 7:
                        messagebox.showinfo("SL Invalid Input", "      Please enter valid exchange rate \nExchange rate needs to be 7 characters long")
                        self.sl_box.delete(0, END)
                        self.sl_box.insert(0, "0.0")
                    elif len(self.sl_box.get()) > 7:
                        messagebox.showinfo("SL Invalid Input", "Please enter valid exchange rate \nNo more than 7 characters long")
                        self.sl_box.delete(0, END)
                        self.sl_box.insert(0, "0.0")
                    elif str1[1] != ".":
                        messagebox.showinfo("SL Invalid Input", "Please enter valid exchange rate \nThe entered value needs to be a float\n                    e.g 1.40232")
                        self.sl_box.delete(0, END)
                        self.sl_box.insert(0, "0.0")
                    else:
                        if dict_data.placetrade_values_holder.get("buysell") == "buy" and self.sl_val >= self.tp_val:
                            messagebox.showinfo("Invalid Request SL", "You cannot set (SL > TP)\n  When position = 'buy'")
                        elif dict_data.placetrade_values_holder.get("buysell") == "sell" and self.tp_val >= self.sl_val:
                            messagebox.showinfo("Invalid Request SL", "You cannot set (TP > SL)\n    When position = 'sell'")
                        else:
                            dict_data.startup_load_values_to_startup()
                            dict_data.st_values_holder["SL"] = round(self.sl_val, 5)
                            dict_data.placetrade_values_holder["SL"] = round(self.sl_val, 5)
                            
                            
                            start_up = open("startup_vars", "wb")
                            pickle.dump(dict_data.st_values_holder, start_up)
                            start_up.close()
                            messagebox.showinfo("SL Changed", "SL has been changed to " + str(self.sl_val))
                except Exception:
                    messagebox.showinfo("SL Error", "Something went wrong" + "\nReseting SL to default values")
                    dict_data.startup_load_values_to_startup()
                    dict_data.st_values_holder["SL"] = 0.0
                    dict_data.placetrade_values_holder["SL"] = 0.0

                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    self.sl_box.delete(0, END) 
                    self.sl_box.insert(0, "0.0")
            except Exception:
                messagebox.showinfo("SL Invalid Input", "SL box accepts only numbers")

        
        
        def check_sl(self):
            try:
                self.sl_val = sl_var.get()
                self.sl_val = float(self.sl_val)
                self.tp_val = tp_var.get()
                self.tp_val = float(self.tp_val)
                str1 = self.sl_box.get()
                bs = bs_radio_val.get()
                try:
                    if self.sl_box.get() == "0.0": 
                        self.validation_check_2 = True
                    elif len(self.sl_box.get()) < 7:
                        messagebox.showinfo("SL Invalid Input", "      Please enter valid exchange rate \nExchange rate needs to be 7 characters long")
                        self.validation_check_2 = False
                        self.sl_box.delete(0, END)
                        self.sl_box.insert(0, "0.0")
                        disable_place_trade(self)
                    elif len(self.sl_box.get()) > 7:
                        messagebox.showinfo("SL Invalid Input", "Please enter valid exchange rate \nNo more than 7 characters long")
                        self.validation_check_2 = False
                        self.sl_box.delete(0, END)
                        self.sl_box.insert(0, "0.0")
                        disable_place_trade(self)
                    elif str1[1] != ".":
                        messagebox.showinfo("SL Invalid Input", "Please enter valid exchange rate \nThe entered value needs to be a float")
                        self.validation_check_2 = False
                        self.sl_box.delete(0, END)
                        self.sl_box.insert(0, "0.0")
                        disable_place_trade(self)
                    else:
                        if bs == "buy" and self.alert_activation == False and self.sl_val > self.tp_val and self.tp_val != 0.0:
                            messagebox.showinfo("Invalid Request SL", "You cannot set (SL > TP)\n   When postion = 'buy'")
                            self.validation_check_2 = False
                            disable_place_trade(self)
                        elif bs == "sell" and self.alert_activation == False and self.tp_val > self.sl_val and self.sl_val != 0.0:
                            messagebox.showinfo("Invalid Request SL", "You cannot set (TP > SL)\n   When postion = 'sell'")
                            self.validation_check_2 = False
                            disable_place_trade(self)
                        elif bs == "":
                            messagebox.showinfo("Invalid Request SL", "Select buy or sell postion to change TP")
                            self.validation_check_2 = False
                            disable_place_trade(self)
                        elif bs == "buy" and self.sl_val >= self.updated_exchange_rate:
                            messagebox.showinfo("Invalid Request SL", "You cannot set (SL > Open Price)\n        When position = 'buy'")
                            self.validation_check_2 = False
                            disable_place_trade(self)
                        elif bs == "sell" and  self.updated_exchange_rate >= self.sl_val:
                            messagebox.showinfo("Invalid Request SL", "You cannot set (Open Price > SL)\n        When postion = 'sell'")
                            self.validation_check_2 = False
                            disable_place_trade(self)
                        else:
                            self.validation_check_2 = True
                            set_alert_disabled(self)
                except Exception:
                    messagebox.showinfo("SL Error", "Something went wrong")
                    self.validation_check_2 = False
                    disable_place_trade(self)
            except Exception:
                messagebox.showinfo("SL Invalid Input", "SL box accepts only numbers")
                self.validation_check_2 = False
                disable_place_trade(self)
        
        
        def check_tp(self):
            try:
                self.tp_val = tp_var.get()
                self.tp_val = float(self.tp_val)
                self.sl_val = sl_var.get()
                self.sl_val = float(self.sl_val)
                str1 = self.tp_box.get()
                bs = bs_radio_val.get()
                try:
                    if self.tp_box.get() == "0.0":
                        self.validation_check = True 
                    elif len(self.tp_box.get()) < 7:
                        messagebox.showinfo("TP Invalid Input", "      Please enter valid exchange rate \nExchange rate needs to be 7 characters long")
                        self.validation_check = False
                        self.tp_box.delete(0, END)
                        self.tp_box.insert(0, "0.0")
                        disable_place_trade(self)
                    elif len(self.tp_box.get()) > 7:
                        messagebox.showinfo("TP Invalid Input", "Please enter valid exchange rate \nNo more than 7 characters long")
                        self.validation_check = False
                        self.tp_box.delete(0, END)
                        self.tp_box.insert(0, "0.0")
                        disable_place_trade(self)
                    elif str1[1] != ".":
                        messagebox.showinfo("TP Invalid Input", "Please enter valid exchange rate \nThe entered value needs to be a float \n       e.g 1.40232")
                        self.validation_check = False
                        self.tp_box.delete(0, END)
                        self.tp_box.insert(0, "0.0")
                        disable_place_trade(self)
                    else:
                        if bs == "buy" and self.sl_val > self.tp_val and self.tp_val != 0.0:
                            messagebox.showinfo("Invalid Request TP", "You cannot set (SL > TP)\n   When position = 'buy'")
                            self.validation_check = False
                            disable_place_trade(self)
                            set_alert_active(self)
                        elif bs == "sell" and self.tp_val > self.sl_val and self.sl_val != 0.0:
                            messagebox.showinfo("Invalid Request TP", "You cannot set (TP > SL)\n   When postion = 'sell'")
                            self.validation_check = False
                            disable_place_trade(self)
                            set_alert_active(self)
                        elif bs == "":
                            messagebox.showinfo("Invalid Request TP", "Select buy or sell postion to change TP")
                            self.validation_check = False 
                            disable_place_trade(self)
                            set_alert_active(self)
                        elif bs == "buy" and self.updated_exchange_rate >= self.tp_val:
                            messagebox.showinfo("Invalid Request TP", "You cannot set (Open Price > TP)\n       When position = 'buy'")
                            self.validation_check = False
                            disable_place_trade(self)
                            set_alert_active(self)
                        elif bs == "sell" and self.tp_val >= self.updated_exchange_rate:
                            messagebox.showinfo("Invalid Request TP", "You cannot set (TP > Open Price)\n       When postion = 'sell'")
                            self.validation_check = False
                            disable_place_trade(self)
                            set_alert_active(self)
                        else:
                            self.validation_check = True
                            set_alert_disabled(self) 
                except Exception:
                    messagebox.showinfo("TP Error", "Something went wrong")
                    self.validation_check = False
                    disable_place_trade(self)
            except Exception:
                messagebox.showinfo("TP Invalid Input", "TP box accepts only numbers")
                self.validation_check = False
                disable_place_trade(self)


        def set_alert_active(self):
            self.alert_activation = True
        
        def set_alert_disabled(self):
            self.alert_activation = False

        # Entry box for the modify balance function
        def enter_balance(self):
            global bal_popup 
            bal_popup = tk.Toplevel(self)
            bal_popup.title("Modify Balance")
            bal_popup.geometry("250x150")
            
            bal_popup_lbl = tk.Label(bal_popup, text="Enter Balance To Your Account")
            bal_popup_lbl.pack(pady=5)

            error_popup_lbl = tk.Label(bal_popup, text="")
            error_popup_lbl.pack(pady=5)

            bal_popup_entry = tk.Entry(bal_popup, width=8, textvariable = balance_val)
            bal_popup_entry.pack(pady=5)

            bal_popup_button = ttk.Button(bal_popup, text="OK", command=lambda:verify_entered_bal_update(self, bal_popup_entry, error_popup_lbl))
            bal_popup_button.pack(pady=5)
            if bal_popup.protocol("WM_DELETE_WINDOW"):
                enable_modify_balance(self)
            
            return bal_popup_entry

        # sends you to a youtube video tutorial
        def yt_link(self):
            webbrowser.open("https://www.youtube.com/watch?v=eJs6MVwIojI")

        # Checks if the value entered in the entry box is a number 
        # Convert any number entered in the box into a real 2 decimal number
        def verify_entered_bal_update(self, bal_popup_entry, error_popup_lbl):
            try:
                if len(bal_popup_entry.get()) <= 8:
                    float(bal_popup_entry.get())
                    self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
                    dict_data.placetrade_values_holder["balance"] = round(balance_val.get(), 2)

                    dict_data.st_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance")
                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    
                    enable_modify_balance(self)
                    bal_popup.destroy()
                elif bal_popup_entry.get() == "":
                    bal_popup.destroy
                else:
                    error_popup_lbl.config(text="Error, maximum of 8 digits can be entered")
            except ValueError:
                error_popup_lbl.config(text="Error, Enter Only Numbers")    
            

        # calculates the position size of a trade based on the parameters passed by a user
        # position size / 30 is the balance that will be deducted from a users balance upon placing a trade
        def trade_position_size(self):
            if dict_data.placetrade_values_holder.get("pair") == "GBP/USD":
                self.usd_to_gbp =  1 / dict_data.placetrade_values_holder.get("convert")
                self.position_size = dict_data.placetrade_values_holder.get("open") * dict_data.placetrade_values_holder.get("lot-size") * self.usd_to_gbp
                self.position_size = self.position_size / 30
                self.position_size = round(self.position_size, 2)
            elif dict_data.placetrade_values_holder.get("pair") == "GBP/CAD":
                self.usd_to_gbp = 1 / dict_data.placetrade_values_holder.get("convert")
                self.position_size =   dict_data.placetrade_values_holder.get("lot-size") / 30
                self.position_size = round(self.position_size, 2)
            elif dict_data.placetrade_values_holder.get("pair") == "EURO/USD":
                self.usd_to_gbp =  1 / dict_data.placetrade_values_holder.get("convert")
                self.position_size = dict_data.placetrade_values_holder.get("lot-size") * self.euro_to_gbp
                self.position_size = self.position_size / 30
                self.position_size = round(self.position_size, 2)
            elif dict_data.placetrade_values_holder.get("pair") == "AUD/USD":
                self.usd_to_gbo = 1 / dict_data.placetrade_values_holder.get("convert")
                self.position_size = dict_data.placetrade_values_holder.get("lot-size") * self.aud_to_gbp
                self.position_size = self.position_size / 20
                self.position_size = round(self.position_size, 2)

            

        # checks if the user has enough funds to cover a trade
        # various actions take place whenever a user's placed trade doesn't meet the criteria
        def check_balance(self):
            min_pos = dict_data.placetrade_values_holder.get("open") * 1000 * self.usd_to_gbp
            min_pos = min_pos / 30
            min_pos = round(min_pos, 2)
            if  min_pos > dict_data.placetrade_values_holder.get("balance"):
                messagebox.showinfo("Inssuficient Balance", "Please add more balance to continue trading")
                enter_balance(self)
                self.validation_check = False
                disable_place_trade(self)
            elif dict_data.placetrade_values_holder.get("balance") <= 0:
                messagebox.showinfo("Inssuficient Balance", "Your account balance is too low\n      Please add more balance")
                enter_balance(self)
                self.validation_check = False
                disable_place_trade(self)
            elif self.position_size > dict_data.placetrade_values_holder.get("balance"):
                messagebox.showinfo("Insufficient Balance", "Not Enough Balance To Place This Trade")
                self.validation_check = False
                disable_place_trade(self)
            else:
                self.validation_check = True
                dict_data.placetrade_values_holder["pos-size"] = self.position_size
                dict_data.placetrade_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance") - dict_data.placetrade_values_holder.get("pos-size")
                dict_data.placetrade_values_holder["balance"] = round(dict_data.placetrade_values_holder["balance"], 2)
                
                dict_data.st_values_holder["pos-size"] = dict_data.placetrade_values_holder.get("pos-size")
                dict_data.st_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance")

                start_up = open("startup_vars", "wb")
                pickle.dump(dict_data.st_values_holder, start_up)
                start_up.close()

                self.text_box.config(text=("£" + str(round(dict_data.placetrade_values_holder.get("balance"), 2))))
                balance_val.set(dict_data.placetrade_values_holder.get("balance"))
            
            
            
        # Changing themes of the application / Light & Dark Modes  
        def theme_mode(self, ld_radio_val):
            radio_val_ld = ld_radio_val.get()
            if radio_val_ld == 1:
                set_light_theme(self)
            elif radio_val_ld == 2:
                set_dark_theme(self)
        
        # sets the app to light mode
        def set_light_theme(self):
            self.main_body.config(bg="#FDFDFD")
            self.banner_lbl.config(bg="#BDBABA", fg="#000000")
            self.tabs_bar.config(bg="#DC7979")
            self.balance_lbl.config(bg="#FDFDFD")
            self.curreny_pair_lbl.config(bg="#FDFDFD")
            self.exchange_lbl.config(bg="#FDFDFD")
            self.lot_size_lbl.config(bg="#FDFDFD")
            self.guide_lbl.config(bg="#FDFDFD")
            self.radio_buy_sell.config(bg="#FDFDFD")

        # sets the app to dark mode
        def set_dark_theme(self):
            self.main_body.config(bg="#BDBABA")
            self.banner_lbl.config(bg="#DC7979", fg="#FDFDFD" )
            self.tabs_bar.config(bg="#BDBABA") 
            self.balance_lbl.config(bg="#ECECEC")
            self.curreny_pair_lbl.config(bg="#ECECEC")
            self.exchange_lbl.config(bg="#ECECEC")
            self.lot_size_lbl.config(bg="#ECECEC")
            self.guide_lbl.config(bg="#ECECEC")
            self.radio_buy_sell.config(bg="#ECECEC")
            
            

        # This function will use the scale and increment it by 500 each time user moves it
        # As I have used ttk insted of tk, it didn't have the same options as tk 
        # therefore this function was necessary for program to work as I wanted it to
        def select_lotsize(self):
            self.int_lot_size_val = int(slider_val.get())
            for minNum, maxNum in lotsize_values:
                if self.int_lot_size_val > minNum and self.int_lot_size_val < maxNum:
                    slider_val.set(maxNum)
                    self.int_lot_size_val = slider_val.get()
                elif self.int_lot_size_val < 500:
                    slider_val.set(0)
                    self.int_lot_size_val = slider_val.get()
            self.lot_size_box.delete(0, "end")
            self.lot_size_box.insert(0, int(slider_val.get()))
            
        
        # displays the upto date exchange rate for a picked curreny pair
        def display_exchange_rate(self):
            if dict_data.st_values_holder.get("is_trade_filed") == True:
                check_display_exchange_rate(self)
                if self.validation_check == True:
                    enable_place_trade(self)
            else:
                 messagebox.showinfo("Trade", "Please file your most recent trade")
                 controller.show_frame(result_raised.result)
            
        # validation check is made whenever 'place trade' button has been clicked by a user
        # all of the paramters are then being saved into a dictionary for a later use
        def place_trade(self):
            import commondata
            while self.validation_check is True:
                check_currency_pair(self)
                if commondata.send_data is True:
                    check_tp(self)
                    check_sl(self)
                    check_buy_sell(self)
                    check_lot_size(self)
                    select_lotsize_entrybox(self)
                    if self.validation_check is True and self.validation_check_2 is True:
                        dict_data.placetrade_values_holder["pair"] = self.currency_pair_combo.get()
                        dict_data.placetrade_values_holder["lot-size"] = self.int_lot_size_val
                        dict_data.placetrade_values_holder["buysell"] = bs_radio_val.get()
                        dict_data.placetrade_values_holder["open"] = self.buysell_exchange
                        dict_data.placetrade_values_holder["convert"] = self.conversion
                        dict_data.placetrade_values_holder["SL"] = self.sl_val
                        dict_data.placetrade_values_holder["SL-Prev"] = self.sl_val
                        dict_data.placetrade_values_holder["TP"] = self.tp_val
                        dict_data.placetrade_values_holder["Bid"] = self.bid_exchange_rate
                        dict_data.placetrade_values_holder["Ask"] = self.ask_exchange_rate

                        trade_position_size(self)

                        dict_data.st_values_holder["pair"] = dict_data.placetrade_values_holder.get("pair")
                        dict_data.st_values_holder["lot-size"] = dict_data.placetrade_values_holder.get("lot-size")
                        dict_data.st_values_holder["buysell"] = dict_data.placetrade_values_holder.get("buysell")
                        dict_data.st_values_holder["open"] = dict_data.placetrade_values_holder.get("open")
                        dict_data.st_values_holder["convert"] = dict_data.placetrade_values_holder.get("convert")
                        dict_data.st_values_holder["SL"] = dict_data.placetrade_values_holder.get("SL")
                        dict_data.st_values_holder["SL-Prev"] = dict_data.placetrade_values_holder.get("SL-Prev")
                        dict_data.st_values_holder["TP"] = dict_data.placetrade_values_holder.get("TP")
                        dict_data.st_values_holder["Bid"] = dict_data.placetrade_values_holder.get("Bid")
                        dict_data.st_values_holder["Ask"] = dict_data.placetrade_values_holder.get("Ask")

                        check_balance(self)
                        if self.validation_check is True:
                            dict_data.is_trade_placed = True
                            dict_data.st_values_holder["is_placed"] = True

                            start_up = open("startup_vars", "wb")
                            pickle.dump(dict_data.st_values_holder, start_up)
                            start_up.close()
                            place_trade_operations(self)
                break

        # some side operations take place whenever trade was successfully placed
        def place_trade_operations(self):
            if dict_data.is_trade_placed is True:
                disable_place_trade(self)
                disable_update_exchange(self)
                disable_modify_balance(self)
                enable_close_trade(self)
                enable_charts(self)
                enable_SL(self)
                enable_TP(self)
                
                
        # clouser exchange rate is being retrived whenever trades is being closed
        # followed by other functions being executed
        def close_trade(self):
            import commondata
            bs = dict_data.placetrade_values_holder.get("buysell")
            if dict_data.placetrade_values_holder.get("pair") == "GBP/USD":
                commondata.get_current_exchange_rate_gbp()
                if commondata.send_data is True: 
                    self.conversion = commondata.temp_exchange_gbp_usd
                    self.usd_to_gbp = self.conversion
                    self.usd_to_gbp = 1 / self.usd_to_gbp
                    if bs == "buy":
                        self.bid_exchange_rate = commondata.gu_bid
                        dict_data.placetrade_values_holder["close"] = self.bid_exchange_rate
                        self.exchange_rate_box.config(text=dict_data.placetrade_values_holder["close"])
                    elif bs == "sell":
                        self.ask_exchange_rate = commondata.gu_ask
                        dict_data.placetrade_values_holder["close"] = self.ask_exchange_rate
                        self.exchange_rate_box.config(text=dict_data.placetrade_values_holder["close"])
            elif dict_data.placetrade_values_holder.get("pair") == "GBP/CAD":
                commondata.get_gbp_cad_exchange_rate()
                if commondata.send_data is True:
                    self.conversion = commondata.temp_exchange_gbp_cad
                    self.usd_to_gbp = self.conversion
                    self.usd_to_gbp = 1 / self.usd_to_gbp
                    if bs == "buy":
                        self.bid_exchange_rate = commondata.gc_bid
                        dict_data.placetrade_values_holder["close"] = self.bid_exchange_rate
                        self.exchange_rate_box.config(text=dict_data.placetrade_values_holder["close"])
                    elif bs == "sell":
                        self.ask_exchange_rate = commondata.gc_ask
                        dict_data.placetrade_values_holder["close"] = self.ask_exchange_rate
                        self.exchange_rate_box.config(text=dict_data.placetrade_values_holder["close"])
            elif dict_data.placetrade_values_holder.get("pair") == "EURO/USD":
                commondata.get_currency_exchange_rate_euro()
                commondata.get_current_exchange_rate_gbp()
                if commondata.send_data is True:
                    self.conversion = commondata.temp_exchange_gbp_usd
                    self.exchange_euro_usd = commondata.temp_exchange_euro_usd
                    self.usd_to_gbp = self.conversion
                    self.usd_to_gbp = 1 / self.usd_to_gbp
                    if bs == "buy":
                        self.bid_exchange_rate = commondata.eu_bid
                        dict_data.placetrade_values_holder["close"] = self.bid_exchange_rate
                        self.exchange_rate_box.config(text=dict_data.placetrade_values_holder["close"])
                    elif bs == "sell":
                        self.ask_exchange_rate = commondata.eu_ask
                        dict_data.placetrade_values_holder["close"] = self.ask_exchange_rate
                        self.exchange_rate_box.config(text=dict_data.placetrade_values_holder["close"])
            elif dict_data.placetrade_values_holder.get("pair") == "AUD/USD":
                commondata.get_aud_usd_exchange_rate()
                commondata.get_current_exchange_rate_gbp()
                if commondata.send_data is True:
                    self.conversion = commondata.temp_exchange_gbp_usd
                    self.exchange_aud_usd = commondata.temp_conversion_aud_gbp
                    self.gbp_usd = self.conversion
                    self.gbp_usd = 1 / self.gbp_usd
                    if bs == "buy":
                        self.bid_exchange_rate = commondata.au_bid
                        dict_data.placetrade_values_holder["close"] = self.bid_exchange_rate
                        self.exchange_rate_box.config(text=dict_data.placetrade_values_holder["close"])
                    elif bs == "sell":
                        self.ask_exchange_rate = commondata.au_ask
                        dict_data.placetrade_values_holder["close"] = self.ask_exchange_rate
                        self.exchange_rate_box.config(text=dict_data.placetrade_values_holder["close"])
            if commondata.send_data is True:
                close_trade_operations(self, balance_val)
                disable_close_trade(self)
                enable_update_exchange(self)
                enable_modify_balance(self)
                disable_charts(self)
                disable_TP(self)
                disable_SL(self)
                self.tp_box.delete(0, END)
                self.sl_box.delete(0, END) 
                self.tp_box.insert(0, "0.0")
                self.sl_box.insert(0, "0.0")
            
        # this function will check the difference between the opening rate and the closing rate
        # based on the difference between these 2 parameters, users balance will gain/loss or remain unchanged
        # balance/loss-gain and others data will be saved into startup dictionary for the next session
        # all the other data for the current trade will be saved into dict_data.filetrade and uploaded into a separated file
        # which can be loaded up on command, in form of a dictionary
        def close_trade_operations(self, balance_val):
            if dict_data.placetrade_values_holder.get("close") > dict_data.placetrade_values_holder.get("open"):# Gain balance
                if dict_data.placetrade_values_holder.get("buysell") == "buy" and dict_data.placetrade_values_holder.get("TP") != 0.0 and dict_data.placetrade_values_holder.get("close") >= dict_data.placetrade_values_holder.get("TP") and self.validate_result_check == False :
                    self.result = dict_data.placetrade_values_holder.get("TP") - dict_data.placetrade_values_holder.get("open") 
                    self.result = self.result * dict_data.placetrade_values_holder.get("lot-size") / dict_data.placetrade_values_holder.get("TP")
                    self.result = round(self.result, 2)
                    dict_data.placetrade_values_holder["loss-gain"] = self.result

                    self.balance = balance_val.get() + dict_data.placetrade_values_holder.get("pos-size")
                    self.balance = self.balance + dict_data.placetrade_values_holder.get("loss-gain")
                    self.balance = round(self.balance, 2)
                    balance_val.set(self.balance)
                    self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
                    dict_data.placetrade_values_holder["balance"] = round(balance_val.get(), 2)

                    dict_data.placetrade_values_holder["close"] = dict_data.placetrade_values_holder["TP"]
                    dict_data.st_values_holder["close"] = dict_data.placetrade_values_holder["close"]
                    dict_data.st_values_holder["is_placed"] = False
                    dict_data.st_values_holder["is_trade_filed"] = False
                    dict_data.st_values_holder["loss-gain"] = dict_data.placetrade_values_holder.get("loss-gain")
                    dict_data.st_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance")

                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    self.validate_result_check = True
                    print("TP Triggered Close > Open")



                elif dict_data.placetrade_values_holder.get("buysell") == "buy" and self.validate_result_check == False:
                    self.result = dict_data.placetrade_values_holder.get("close") - dict_data.placetrade_values_holder.get("open") 
                    self.result = self.result * dict_data.placetrade_values_holder.get("lot-size") * self.usd_to_gbp
                    self.result = round(self.result, 2)
                    dict_data.placetrade_values_holder["loss-gain"] = self.result

                    self.balance = balance_val.get() + dict_data.placetrade_values_holder.get("pos-size")
                    self.balance = self.balance + dict_data.placetrade_values_holder.get("loss-gain")
                    self.balance = round(self.balance, 2)
                    balance_val.set(self.balance)
                    self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
                    dict_data.placetrade_values_holder["balance"] = round(balance_val.get(), 2)

                    dict_data.st_values_holder["is_placed"] = False
                    dict_data.st_values_holder["is_trade_filed"] = False
                    dict_data.st_values_holder["loss-gain"] = dict_data.placetrade_values_holder.get("loss-gain")
                    dict_data.st_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance")

                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    self.validate_result_check = True
                    print("Normal Close > Open")


                    
                elif dict_data.placetrade_values_holder.get("buysell") == "sell" and dict_data.placetrade_values_holder.get("SL") != 0.0 and dict_data.placetrade_values_holder.get("close") >= dict_data.placetrade_values_holder.get("SL") and self.validate_result_check == False:# Lose balance
                    self.result = dict_data.placetrade_values_holder.get("open") - dict_data.placetrade_values_holder.get("SL")
                    self.result = self.result * dict_data.placetrade_values_holder.get("lot-size") / dict_data.placetrade_values_holder.get("SL")
                    self.result = round(self.result, 2)
                    dict_data.placetrade_values_holder["loss-gain"] = self.result

                    self.balance = balance_val.get() + dict_data.placetrade_values_holder.get("pos-size")
                    self.balance = self.balance + dict_data.placetrade_values_holder.get("loss-gain")
                    self.balance = round(self.balance, 2)
                    balance_val.set(self.balance)
                    self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
                    dict_data.placetrade_values_holder["balance"] = round(balance_val.get(), 2)

                    dict_data.placetrade_values_holder["close"] = dict_data.placetrade_values_holder["SL"]
                    dict_data.st_values_holder["close"] = dict_data.placetrade_values_holder["close"]
                    dict_data.st_values_holder["is_placed"] = False
                    dict_data.st_values_holder["is_trade_filed"] = False
                    dict_data.st_values_holder["loss-gain"] = dict_data.placetrade_values_holder.get("loss-gain")
                    dict_data.st_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance")

                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    self.validate_result_check = True
                    print("SL Triggered Close > Open")


                elif dict_data.placetrade_values_holder.get("buysell") == "sell" and self.validate_result_check == False:# Lose balance
                    self.result = dict_data.placetrade_values_holder.get("open") - dict_data.placetrade_values_holder.get("close") 
                    self.result = self.result * dict_data.placetrade_values_holder.get("lot-size") * self.usd_to_gbp
                    self.result = round(self.result, 2)
                    dict_data.placetrade_values_holder["loss-gain"] = self.result

                    self.balance = balance_val.get() + dict_data.placetrade_values_holder.get("pos-size")
                    self.balance = self.balance + dict_data.placetrade_values_holder.get("loss-gain")
                    self.balance = round(self.balance, 2)
                    balance_val.set(self.balance)
                    self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
                    dict_data.placetrade_values_holder["balance"] = round(balance_val.get(), 2)

                    dict_data.st_values_holder["is_placed"] = False
                    dict_data.st_values_holder["is_trade_filed"] = False
                    dict_data.st_values_holder["loss-gain"] = dict_data.placetrade_values_holder.get("loss-gain")
                    dict_data.st_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance")

                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    self.validate_result_check = True
                    print("Normal Close > Open")
                    
                    
                dict_data.placetrade_values_to_filedata()
                dict_data.filetrade = open("ft_data", "wb")
                pickle.dump(dict_data.ft_data, dict_data.filetrade)
                dict_data.filetrade.close()

                
            if dict_data.placetrade_values_holder.get("open") > dict_data.placetrade_values_holder.get("close"):
                if dict_data.placetrade_values_holder.get("buysell") == "buy" and dict_data.placetrade_values_holder.get("SL") != 0.0 and dict_data.placetrade_values_holder.get("SL") >= dict_data.placetrade_values_holder.get("close") and self.validate_result_check == False:
                    self.result = dict_data.placetrade_values_holder.get("SL") - dict_data.placetrade_values_holder.get("open")
                    self.result = self.result * dict_data.placetrade_values_holder.get("lot-size") / dict_data.placetrade_values_holder.get("SL")
                    self.result = round(self.result, 2)
                    dict_data.placetrade_values_holder["loss-gain"] = self.result

                    self.balance =  balance_val.get() + dict_data.placetrade_values_holder.get("pos-size")
                    self.balance = self.balance + dict_data.placetrade_values_holder.get("loss-gain")
                    self.balance = round(self.balance, 2)
                    balance_val.set(self.balance)
                    self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
                    dict_data.placetrade_values_holder["balance"] = round(balance_val.get(), 2)

                    dict_data.placetrade_values_holder["close"] = dict_data.placetrade_values_holder["SL"]
                    dict_data.st_values_holder["close"] = dict_data.placetrade_values_holder["close"]
                    dict_data.st_values_holder["is_trade_filed"] = False
                    dict_data.st_values_holder["is_placed"] = False
                    dict_data.st_values_holder["loss-gain"] = dict_data.placetrade_values_holder.get("loss-gain")
                    dict_data.st_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance")

                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    self.validate_result_check = True
                    print("SL Triggered Open > Close")
                
                elif dict_data.placetrade_values_holder.get("buysell") == "buy" and self.validate_result_check == False:
                    self.result = dict_data.placetrade_values_holder.get("close") - dict_data.placetrade_values_holder.get("open")
                    self.result = self.result * dict_data.placetrade_values_holder.get("lot-size") * self.usd_to_gbp
                    self.result = round(self.result, 2)
                    dict_data.placetrade_values_holder["loss-gain"] = self.result

                    self.balance =  balance_val.get() + dict_data.placetrade_values_holder.get("pos-size")
                    self.balance = self.balance + dict_data.placetrade_values_holder.get("loss-gain")
                    self.balance = round(self.balance, 2)
                    balance_val.set(self.balance)
                    self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
                    dict_data.placetrade_values_holder["balance"] = round(balance_val.get(), 2)
                    dict_data.st_values_holder["is_trade_filed"] = False
                    dict_data.st_values_holder["is_placed"] = False
                    dict_data.st_values_holder["loss-gain"] = dict_data.placetrade_values_holder.get("loss-gain")
                    dict_data.st_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance")

                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    self.validate_result_check = True
                    print("Normal Open > Close")
                    
                elif dict_data.placetrade_values_holder.get("buysell") == "sell" and dict_data.placetrade_values_holder.get("TP") != 0.0 and dict_data.placetrade_values_holder.get("TP") >= dict_data.placetrade_values_holder.get("close") and self.validate_result_check == False:
                    self.result = dict_data.placetrade_values_holder.get("open") - dict_data.placetrade_values_holder.get("TP")
                    self.result = self.result * dict_data.placetrade_values_holder.get("lot-size") / dict_data.placetrade_values_holder.get("TP")
                    self.result = round(self.result, 2)
                    dict_data.placetrade_values_holder["loss-gain"] = self.result

                    self.balance =  balance_val.get() + dict_data.placetrade_values_holder.get("pos-size")
                    self.balance = self.balance + dict_data.placetrade_values_holder.get("loss-gain")
                    self.balance = round(self.balance, 2)
                    balance_val.set(self.balance)
                    self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
                    dict_data.placetrade_values_holder["balance"] = round(balance_val.get(), 2)

                    dict_data.placetrade_values_holder["close"] = dict_data.placetrade_values_holder["TP"]
                    dict_data.st_values_holder["close"] = dict_data.placetrade_values_holder["close"]
                    dict_data.st_values_holder["is_trade_filed"] = False
                    dict_data.st_values_holder["is_placed"] = False
                    dict_data.st_values_holder["loss-gain"] = dict_data.placetrade_values_holder.get("loss-gain")
                    dict_data.st_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance")

                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    self.validate_result_check = True
                    print("TP Triggered Open > Close")



                elif dict_data.placetrade_values_holder.get("buysell") == "sell" and self.validate_result_check == False:
                    self.result = dict_data.placetrade_values_holder.get("open") - dict_data.placetrade_values_holder.get("close")
                    self.result = self.result * dict_data.placetrade_values_holder.get("lot-size") * self.usd_to_gbp
                    self.result = round(self.result, 2)
                    dict_data.placetrade_values_holder["loss-gain"] = self.result

                    self.balance =  balance_val.get() + dict_data.placetrade_values_holder.get("pos-size")
                    self.balance = self.balance + dict_data.placetrade_values_holder.get("loss-gain")
                    self.balance = round(self.balance, 2)
                    balance_val.set(self.balance)
                    self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
                    dict_data.placetrade_values_holder["balance"] = round(balance_val.get(), 2)
                    dict_data.st_values_holder["is_trade_filed"] = False
                    dict_data.st_values_holder["is_placed"] = False
                    dict_data.st_values_holder["loss-gain"] = dict_data.placetrade_values_holder.get("loss-gain")
                    dict_data.st_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance")

                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    self.validate_result_check = True
                    print("Normal Open > Close")

                dict_data.placetrade_values_to_filedata()
                dict_data.filetrade = open("ft_data", "wb")
                pickle.dump(dict_data.ft_data, dict_data.filetrade)
                dict_data.filetrade.close()
                
                
            if dict_data.placetrade_values_holder.get("open") == dict_data.placetrade_values_holder.get("close") and self.validate_result_check == False:
                if dict_data.placetrade_values_holder.get("buysell") == "buy" or dict_data.placetrade_values_holder.get("buysell") == "sell":
                    self.balance =  balance_val.get() + dict_data.placetrade_values_holder.get("pos-size")
                    self.result = round(self.result, 2)
                    dict_data.placetrade_values_holder["loss-gain"] = self.result
                    
                    self.balance =  balance_val.get() + dict_data.placetrade_values_holder.get("pos-size")
                    self.balance = round(self.balance, 2)
                    balance_val.set(self.balance)
                    dict_data.placetrade_values_holder["loss-gain"] = 0
                    self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
                    dict_data.placetrade_values_holder["balance"] = round(balance_val.get(), 2)
                    dict_data.st_values_holder["is_trade_filed"] = False
                    dict_data.st_values_holder["is_placed"] = False
                    dict_data.st_values_holder["loss-gain"] = dict_data.placetrade_values_holder.get("loss-gain")
                    dict_data.st_values_holder["balance"] = dict_data.placetrade_values_holder.get("balance")

                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    self.validate_result_check = True
            
                    
                dict_data.placetrade_values_to_filedata()
                dict_data.filetrade = open("ft_data", "wb")
                pickle.dump(dict_data.ft_data, dict_data.filetrade)
                dict_data.filetrade.close()
            self.validate_result_check = False
                
                
        
        # enablers & disabler operations for buttons
        def enable_place_trade(self):
            self.place_trade_button.config(state="normal")

        def disable_place_trade(self):
            self.place_trade_button.config(state="disabled")

        def enable_close_trade(self):
            self.close_trade_button.config(state="normal")

        def disable_close_trade(self):
            self.close_trade_button.config(state="disabled")
        
        def enable_update_exchange(self):
            self.update_exchange_button.config(state="normal")
        
        def disable_update_exchange(self):
            self.update_exchange_button.config(state="disabled")
        
        def enable_modify_balance(self):
            self.mod_bal_button.config(state="normal")
        
        def disable_modify_balance(self):
            self.mod_bal_button.config(state="disabled")
        
        def enable_charts(self):
            self.upload_charts.config(state="normal")
        
        def disable_charts(self):
            self.upload_charts.config(state="disabled")

        def enable_SL(self):
            self.sl_change_button.config(state="normal")

        def disable_SL(self):
            self.sl_change_button.config(state="disabled")
        
        def enable_TP(self):
            self.tp_change_button.config(state="normal")

        def disable_TP(self):
            self.tp_change_button.config(state="disabled")
        
        
        # Logic checks necessary to see if the user filled out every box  
        # checks; currency-pair, lot-size, buy&sell order, update exchange, current balance
        # checks if the currency has been selected and than saves both the exchange-rate & currency pair into a dictionary for further use
        def check_currency_pair(self):
            bs = bs_radio_val.get()
            import commondata
            commondata.get_current_exchange_rate_gbp()
            self.conversion = commondata.temp_exchange_gbp_usd
            if self.currency_pair_combo.get() == "":
                messagebox.showinfo("Select Pair", "Please Select Currency Pair")
                disable_place_trade(self)
                self.validation_check = False
            elif self.currency_pair_combo.get() == "GBP/USD":
                self.bid_exchange_rate = commondata.gu_bid
                self.ask_exchange_rate = commondata.gu_ask
                if bs == "buy":
                    self.buysell_exchange = self.bid_exchange_rate
                    self.exchange_rate_box.config(text=self.buysell_exchange)
                    self.validation_check = True
                elif bs == "sell":
                    self.buysell_exchange = self.ask_exchange_rate
                    self.exchange_rate_box.config(text=self.buysell_exchange)
                    self.validation_check = True
                else:
                    disable_place_trade(self)
                    messagebox.showinfo("Position", "Please Select Buy or Sell Position")
                    self.validation_check = False
            elif self.currency_pair_combo.get() == "EURO/USD":
                commondata.get_currency_exchange_rate_euro()
                commondata.get_euro_gbp_conversion()
                self.euro_to_gbp = commondata.temp_conversion_gbp_usd
                self.exchange_euro_usd = commondata.temp_exchange_euro_usd
                self.bid_exchange_rate = commondata.eu_bid
                self.ask_exchange_rate = commondata.eu_ask
                if bs == "buy":
                    self.buysell_exchange = self.bid_exchange_rate
                    self.exchange_rate_box.config(text=self.buysell_exchange)
                    self.validation_check = True  
                elif bs == "sell":
                    self.buysell_exchange = self.ask_exchange_rate
                    self.exchange_rate_box.config(text=self.buysell_exchange)
                    self.validation_check = True  
                else:
                    disable_place_trade(self)
                    messagebox.showinfo("Position", "Please Select Buy or Sell Position")
                    self.validation_check = False
            elif self.currency_pair_combo.get() == "GBP/CAD":
                commondata.get_gbp_cad_exchange_rate()
                self.exchange_gbp_cad = commondata.temp_exchange_gbp_cad
                self.bid_exchange_rate = commondata.gc_bid
                self.ask_exchange_rate = commondata.gc_ask
                if bs == "buy":
                    self.buysell_exchange = self.bid_exchange_rate
                    self.exchange_rate_box.config(text=self.buysell_exchange)
                    self.validation_check = True
                elif bs == "sell":
                    self.buysell_exchange = self.ask_exchange_rate
                    self.exchange_rate_box.config(text=self.buysell_exchange)
                    self.validation_check = True
                else:
                    disable_place_trade(self)
                    messagebox.showinfo("Position", "Please Select Buy or Sell Position")
                    self.validation_check = False
            elif self.currency_pair_combo.get() == "AUD/USD":
                commondata.get_aud_usd_exchange_rate()
                commondata.get_aud_gbp_conversion()
                self.exchange_aud_usd = commondata.temp_exchange_aud_usd
                self.aud_to_gbp = commondata.temp_conversion_aud_gbp
                self.bid_exchange_rate = commondata.au_bid
                self.ask_exchange_rate = commondata.au_ask
                if bs == "buy":
                    self.buysell_exchange = self.bid_exchange_rate
                    self.exchange_rate_box.config(text=self.buysell_exchange)
                    self.validation_check = True
                elif bs == "sell":
                    self.buysell_exchange = self.ask_exchange_rate
                    self.exchange_rate_box.config(text=self.buysell_exchange)
                    self.validation_check = True
                else:
                    disable_place_trade(self)
                    messagebox.showinfo("Position", "Please Select Buy or Sell Position")
                    self.validation_check = False
                
        def check_if_equal_to_sl(self):
            import commondata
            pos = dict_data.placetrade_values_holder.get("buysell")
            if dict_data.placetrade_values_holder.get("pair") == "EURO/USD":
                commondata.get_currency_exchange_rate_euro_startup()
                self.updated_exchange_rate = commondata.temp_exchange_euro_usd
                if self.updated_exchange_rate >= dict_data.placetrade_values_holder.get("SL") and pos == "sell":
                    messagebox.showinfo("Trade Closed", "Your stop-loss was triggered")
                    close_trade(self)
                elif self.updated_exchange_rate <= dict_data.placetrade_values_holder.get("SL") and pos == "buy":
                    messagebox.showinfo("Trade Closed", "Your stop-loss was triggered")
                    close_trade(self)
            elif dict_data.placetrade_values_holder.get("pair") == "GBP/USD":
                commondata.get_current_exchange_rate_gbp_startup()
                self.updated_exchange_rate = float(commondata.temp_exchange_gbp_usd)
                if self.updated_exchange_rate >= dict_data.placetrade_values_holder.get("SL") and pos == "sell":
                    messagebox.showinfo("Trade Closed", "Your stop-loss was triggered")
                    close_trade(self)
                elif self.updated_exchange_rate <= dict_data.placetrade_values_holder.get("SL") and pos == "buy":
                    messagebox.showinfo("Trade Closed", "Your stop-loss was triggered")
                    close_trade(self)
            elif dict_data.placetrade_values_holder.get("pair") == "AUD/USD":
                commondata.get_aud_usd_exchange_rate_startup()
                self.updated_exchange_rate = commondata.temp_exchange_aud_usd
                if self.updated_exchange_rate >= dict_data.placetrade_values_holder.get("SL") and pos == "sell":
                    messagebox.showinfo("Trade Closed", "Your stop-loss was triggered")
                    close_trade(self)
                elif self.updated_exchange_rate <= dict_data.placetrade_values_holder.get("SL") and pos == "buy":
                    messagebox.showinfo("Trade Closed", "Your stop-loss was triggered")
                    close_trade(self)
            elif dict_data.placetrade_values_holder.get("pair") == "GBP/USD":
                commondata.get_gbp_cad_exchange_rate_startup()
                self.updated_exchange_rate = commondata.temp_exchange_gbp_cad
                if self.updated_exchange_rate >= dict_data.placetrade_values_holder.get("SL") and pos == "sell":
                    messagebox.showinfo("Trade Closed", "Your stop-loss was triggered")
                    close_trade(self)
                elif self.updated_exchange_rate <= dict_data.placetrade_values_holder.get("SL") and pos == "buy":
                    messagebox.showinfo("Trade Closed", "Your stop-loss was triggered")
                    close_trade(self)


        def check_display_exchange_rate(self):
            import commondata
            if self.currency_pair_combo.get() == "":
                messagebox.showinfo("Select Pair", "Please Select Currency Pair")
                disable_place_trade(self)
                self.validation_check = False
            elif self.currency_pair_combo.get() == "GBP/USD":
                commondata.get_current_exchange_rate_gbp()
                self.conversion = commondata.temp_exchange_gbp_usd
                self.updated_exchange_rate = self.conversion
                self.exchange_rate_box.config(text=self.updated_exchange_rate)
                self.validation_check = True
            elif self.currency_pair_combo.get() == "GBP/CAD":
                commondata.get_gbp_cad_exchange_rate()
                self.conversion = commondata.temp_exchange_gbp_cad
                self.updated_exchange_rate = self.conversion
                self.exchange_rate_box.config(text=self.updated_exchange_rate)
                self.validation_check = True
            elif self.currency_pair_combo.get() == "EURO/USD":
                commondata.get_currency_exchange_rate_euro()
                self.exchange_euro_usd = commondata.temp_exchange_euro_usd
                self.updated_exchange_rate = self.exchange_euro_usd
                self.exchange_rate_box.config(text=self.updated_exchange_rate)
                self.validation_check = True
            elif self.currency_pair_combo.get() == "AUD/USD":
                commondata.get_aud_usd_exchange_rate()
                self.exchange_aud_usd = commondata.temp_exchange_aud_usd
                self.updated_exchange_rate = self.exchange_aud_usd
                self.exchange_rate_box.config(text=self.updated_exchange_rate)
                self.validation_check = True  

        # checks if lot-size was selected and than saves it to the dictionary for further use
        def check_lot_size(self):
            try:
                if self.validation_check is True:
                    if self.int_lot_size_val == 0 and slider_entry_box.get() == 0:
                        messagebox.showinfo("Select Lot-Size", "Lot-Size Entry Box Is Empty")
                        self.validation_check = False
                        disable_place_trade(self)    
                    else:
                        self.int_lot_size_val = int(slider_val.get())
                        self.validation_check = True
            except Exception:
                messagebox.showinfo("Lot-Size", "Something Went Wrong")
                self.validation_check = False 
            
            
        # lets a user enter lot-size manually, then does some validation checks on the users entry
        def select_lotsize_entrybox(self):
            try:
                if self.int_lot_size_val != slider_entry_box.get():
                    try:
                        self.int_lot_size_val = int(slider_entry_box.get())
                        if self.int_lot_size_val < 1000:
                            messagebox.showinfo("Insufficient Lot-Size", "Minimal Lot-Size Allowed Is 1000")
                            self.validation_check = False
                            disable_place_trade(self)
                        else:
                            self.validation_check = True
                    except Exception:
                        messagebox.showinfo("Lot-Size", "Lot-Size Entry Box Only Accepts Numbers")
                        self.validation_check = False            
            except Exception:
                messagebox.showinfo("Lot-Size", "Lot-Size Entry Box Only Accepts Numbers")
                self.validation_check = False 


        # checks if a position order is a buy or sell and saves it to a dictionary for further use
        def check_buy_sell(self):
            if self.validation_check is True:
                bs = bs_radio_val.get()
                if bs == "buy":
                    self.validation_check = True
                elif bs == "sell":
                    self.validation_check = True
                else:
                    self.validation_check = False
                    disable_place_trade(self)
                    messagebox.showinfo("Position", "Please Select Buy or Sell Position")

        # uploads any charts that were uploaded by a user
        def upload_all_charts(self):
            if dict_data.placetrade_values_holder["4-hour"] == "" or dict_data.placetrade_values_holder["1-hour"] == "" or dict_data.placetrade_values_holder["15-min"] == "":
                q_answer = messagebox.askyesno("Missing Charts", "One or more charts have not been uploaded\n              Do you wish to continue ?")
                if q_answer == False:
                    pass
                else:
                    dict_data.placetrade_values_to_startup()
                    
                    start_up = open("startup_vars", "wb")
                    pickle.dump(dict_data.st_values_holder, start_up)
                    start_up.close()
                    messagebox.showinfo("Updated", "Charts Were Successfully Uploaded")
            elif dict_data.placetrade_values_holder["4-hour"] != "" and dict_data.placetrade_values_holder["1-hour"] != "" and dict_data.placetrade_values_holder["15-min"] != "":
                dict_data.placetrade_values_to_startup()
                    
                start_up = open("startup_vars", "wb")
                pickle.dump(dict_data.st_values_holder, start_up)
                start_up.close()
                messagebox.showinfo("Updated", "Charts Were Successfully Uploaded")
            else:
                messagebox.showinfo("No Charts", "You haven't selected any charts to upload")
    
        
        # Start-up functions, initializes all of the variables to default
        def startup(self):
            dict_data.placetrade_values_holder["balance"] = (balance_val.get())
            if dict_data.is_trade_placed is True:
                trade_is_open(self)
            elif dict_data.is_trade_placed is False: 
                trade_is_closed(self)
        
        # The application starts with no trade placed
        def trade_is_closed(self):
            dict_data.startup_load_values_to_startup()
            enable_modify_balance(self)
            enable_update_exchange(self)
            disable_close_trade(self)
            disable_charts(self)
            disable_TP(self)
            disable_SL(self)
            self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
            

        # The application starts with a trade being placed (Normally)
        def trade_is_open(self):
            dict_data.startupload_values_to_placetrade()
            dict_data.placetrade_values_to_startup()
            print(f"Startup_dict   {dict_data.st_values_holder.values()}")
            print(f"Placetrade_dict   {dict_data.placetrade_values_holder.values()}")
            self.usd_to_gbp = 1 / dict_data.placetrade_values_holder.get("convert")
            self.exchange_rate_box.config(text=dict_data.get_dict_data["open"])
            self.text_box.config(text=("£" + str(round(balance_val.get(), 2))))
            self.lot_size_box.config(slider_entry_box.set(dict_data.placetrade_values_holder.get("lot-size")))
            self.currency_pair_combo.set(dict_data.placetrade_values_holder.get("pair"))
            bs_radio_val.set(dict_data.placetrade_values_holder.get("buysell"))
            tp_var.set(dict_data.st_values_holder["TP"])
            sl_var.set(dict_data.st_values_holder["SL"])
            disable_place_trade(self)
            disable_modify_balance(self)
            disable_update_exchange(self)
            enable_close_trade(self)
            enable_charts(self)
            enable_SL(self)
            enable_TP(self)
            check_if_equal_to_sl(self)
            
            
        startup(self)




    


