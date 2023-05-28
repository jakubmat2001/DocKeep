from tkinter import EXCEPTION, messagebox
from tkinter import ttk, filedialog
from tkinter.constants import END, INSERT
from PIL import ImageTk, Image
import pickle
import tkinter as tk
import string
import retrivables.dict_data as dict_data

# various fonts used for label widgets
App_font = ("Sans-Serif", 13)
Body_font = ("Sans-Serif", 9)

# a one hour tab which holds some of the opeartions for uploading 1-hour charts
class one_hour(tk.Frame):
    def __init__(self, parent, controller):
        import pages.mainpage_raised as mainpage_raised, pages.four_hour_raised as four_hour_raised, pages.fifteen_min_raised as fifteen_min_raised, retrivables.result_raised as result_raised
        tk.Frame.__init__(self, parent)

        self.test_img = ""
        self.resizingImg = ""
        self.new_img = ""
        
        self.one_hour_body = tk.Frame(self, bg="#FDFDFD", padx=20, pady=20)
        self.one_hour_body.grid(row=2, column=0, sticky="nsew")

        self.tabs_bar = tk.Frame(self, bg="#DC7979")
        self.tabs_bar.grid(row=0, column=0, sticky="we")

        self.banner_lbl = tk.Label(self, text="One Hour",font=App_font ,width=120, height=5, bg="#BDBABA")
        self.banner_lbl.grid(row=1, column=0 )

        self.button11 = tk.Button(self.tabs_bar, text="Main", command=lambda: controller.show_frame(mainpage_raised.mainpage), borderwidth=1, relief="solid")
        self.button11.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

        self.button12 = tk.Button(self.tabs_bar, text="4 Hour", command=lambda: controller.show_frame(four_hour_raised.four_hour), borderwidth=1, relief="solid")
        self.button12.grid(row=0, column=2, padx=(5, 5), pady=(5, 5))

        self.button13 = tk.Button(self.tabs_bar, text="1 Hour", command=lambda: controller.show_frame(one_hour), borderwidth=1, relief="solid")
        self.button13.grid(row=0, column=3, padx=(5, 5), pady=(5, 5))

        self.button14 = tk.Button(self.tabs_bar, text="15 Min", command=lambda: controller.show_frame(fifteen_min_raised.fifteen_min), borderwidth=1, relief="solid")
        self.button14.grid(row=0, column=4, padx=(5, 5), pady=(5, 5))

        self.button15 = tk.Button(self.tabs_bar, text="Result", command=lambda: controller.show_frame(result_raised.result), borderwidth=1, relief="solid")
        self.button15.grid(row=0, column=5, padx=(5, 5), pady=(5, 5))

        self.disp_1_hour = tk.Label(self.one_hour_body, width=135, height=33, image=self.test_img, text="This Chart Is Currently Empty \nClick 'Add 1-Hour Chart' To Add One" ,relief="solid", borderwidth=1)
        self.disp_1_hour.grid(rowspan=20, columnspan=5)

        self.o_hour_button = ttk.Button(self.one_hour_body, text="Add 1-Hour\n      Chart" ,command=lambda: one_hour.add_1_hour(self))
        self.o_hour_button.grid(row=10, column=5, padx=(20, 0))

        self.clear_1_hour = ttk.Button(self.one_hour_body, text="Clear\nChart", command=lambda: one_hour.clear_chart(self))
        self.clear_1_hour.grid(row=11, column=5,  padx=(20, 0))

        # places added chart on a image-placeholder label if it was uploaded in the past
        def get_img(self):
            try:
                if dict_data.st_values_holder.get("is_placed") == True:
                    self.test_img = Image.open(dict_data.placetrade_values_holder.get("1-hour"))
                    self.resizingImg = self.test_img.resize((950, 490), Image.ANTIALIAS)
                    self.new_img = ImageTk.PhotoImage(self.resizingImg)
                    self.disp_1_hour.config(width=950, height=490 ,image=self.new_img, text="")
                else:
                    dict_data.filetrade = open("ft_data", "rb")
                    dict_data.get_filedict_data = pickle.load(dict_data.filetrade)

                    self.test_img = Image.open(dict_data.get_filedict_data.get("1-hour"))
                    self.resizingImg = self.test_img.resize((950, 490), Image.ANTIALIAS)
                    self.new_img = ImageTk.PhotoImage(self.resizingImg)
                    self.disp_1_hour.config(width=950, height=490 ,image=self.new_img, text="")
            except Exception:
                pass
        get_img(self)
        
    # adds a 1 hour chart selected by a user
    def add_1_hour(self):
        try:
            if dict_data.st_values_holder.get("is_placed") == False and dict_data.st_values_holder.get("is_trade_filed") == False:
                messagebox.showinfo("Closed", "         Unable to add a chart\n Can only add while trade is placed")
            elif dict_data.st_values_holder.get("is_placed") == False:
                messagebox.showinfo("Not Open", "Please place a trade to add a chart")
            else:
                filename = tk.filedialog.askopenfile(initialdir="Desktop", title="Select File", filetypes=(("PNG Files", "*.png"),("JPG Files", "*.jpg")))
                dict_data.placetrade_values_holder["1-hour"] = filename.name
                self.test_img = Image.open(dict_data.placetrade_values_holder.get("1-hour"))
                self.resizingImg = self.test_img.resize((950, 490), Image.ANTIALIAS)
                self.new_img = ImageTk.PhotoImage(self.resizingImg)
                self.disp_1_hour.config(width=950, height=490 ,image=self.new_img)
        except Exception:
            messagebox.showinfo("Error", "Failed to load the image")

    # clears and removes a 1 hour chart
    def clear_chart(self):
        self.disp_1_hour.config(image="", text="This Chart Is Currently Empty \nClick 'Add 1-hour Chart' To Add One", width=135, height=33)
        
        dict_data.placetrade_values_holder["1-hour"] = ""

        dict_data.filetrade = open("ft_data", "rb")
        dict_data.get_filedict_data = pickle.load(dict_data.filetrade)

        start_vars = open("startup_vars", "rb")
        dict_data.get_dict_data = pickle.load(start_vars)
        
        dict_data.startup_load_values_to_startup()
        dict_data.st_values_holder["1-hour"] = ""

        dict_data.fileload_values_to_filedata()
        dict_data.ft_data["1-hour"] = ""

        dict_data.filetrade = open("ft_data", "wb")
        pickle.dump(dict_data.ft_data, dict_data.filetrade)
        dict_data.filetrade.close()

        start_up = open("startup_vars", "wb")
        pickle.dump(dict_data.st_values_holder, start_up)
        start_up.close()