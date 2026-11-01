import os
import shutil
import sys
from pathlib import Path
from tkinter import EXCEPTION, messagebox
from tkinter import ttk, filedialog
from tkinter.constants import END, INSERT
from PIL import ImageTk, Image
import pickle
import tkinter as tk
import string
import retrivables.dict_data as dict_data
from retrivables.helpers import data_path

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

        self.tabs_bar = tk.Frame(self, bg="#DC7979", width=110)
        self.tabs_bar.grid(row=0, column=0, sticky="we")

        self.banner_lbl = tk.Label(self, text="One Hour",font=App_font ,width=110, height=5, bg="#BDBABA")
        self.banner_lbl.grid(row=1, column=0, sticky="we")

        self.button11 = tk.Button(self.tabs_bar, text="Main", command=lambda: controller.show_frame(mainpage_raised.mainpage), justify="center", 
                                pady=3, borderwidth=1, relief="groove")
        self.button11.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

        self.button12 = tk.Button(self.tabs_bar, text="4 Hour", command=lambda: controller.show_frame(four_hour_raised.four_hour), justify="center", 
                                pady=3, borderwidth=1, relief="groove")
        self.button12.grid(row=0, column=2, padx=(5, 5), pady=(5, 5))

        self.button13 = tk.Button(self.tabs_bar, text="1 Hour", command=lambda: controller.show_frame(one_hour), justify="center", 
                                pady=3, borderwidth=1, relief="groove")
        self.button13.grid(row=0, column=3, padx=(5, 5), pady=(5, 5))

        self.button14 = tk.Button(self.tabs_bar, text="15 Min", command=lambda: controller.show_frame(fifteen_min_raised.fifteen_min), justify="center", 
                                pady=3, borderwidth=1, relief="groove")
        self.button14.grid(row=0, column=4, padx=(5, 5), pady=(5, 5))

        self.button15 = tk.Button(self.tabs_bar, text="Result", command=lambda: controller.show_frame(result_raised.result), justify="center", 
                                pady=3, borderwidth=1, relief="groove")
        self.button15.grid(row=0, column=5, padx=(5, 5), pady=(5, 5))

        self.disp_1_hour = tk.Label(self.one_hour_body, width=110, height=33, image=self.test_img, text="This Chart Is Currently Empty \nClick 'Add 1-Hour Chart' To Add One" ,relief="solid", borderwidth=1)
        self.disp_1_hour.grid(rowspan=20, columnspan=5)

        self.o_hour_button = tk.Button(self.one_hour_body, text="Add 1-Hour\nChart" ,command=lambda: one_hour.add_1_hour(self), justify="center")
        self.o_hour_button.grid(row=10, column=5, padx=(20, 0))

        self.clear_1_hour = tk.Button(self.one_hour_body, text="Clear\nChart", command=lambda: one_hour.clear_chart(self), justify="center")
        self.clear_1_hour.grid(row=11, column=5,  padx=(20, 0))

        # places added chart on a image-placeholder label if it was uploaded in the past
        def get_img(self):
            try:
                if dict_data.st_values_holder.get("is_placed") is True:
                    image_path = dict_data.placetrade_values_holder.get("1-hour")
                else:
                    with open(data_path("ft_data"), "rb") as filetrade:
                        dict_data.get_filedict_data = pickle.load(filetrade)

                    image_path = dict_data.get_filedict_data.get("1-hour")

                if not image_path:
                    return

                with Image.open(image_path) as image:
                    resized = image.resize(
                        (1000, 530),
                        getattr(Image, "Resampling", Image).LANCZOS
                    )
                    self.new_img = ImageTk.PhotoImage(resized)

                self.disp_1_hour.config(
                    width=1000,
                    height=530,
                    image=self.new_img,
                    text=""
                )

            except Exception as e:
                print("1-hour chart loading error:", repr(e))

        get_img(self)
        
    # adds a 1 hour chart selected by a user
    def add_1_hour(self):
        try:
            if (
                dict_data.st_values_holder.get("is_placed") is False
                and dict_data.st_values_holder.get("is_trade_filed") is False
            ):
                messagebox.showinfo(
                    "Closed",
                    "Unable to add a chart\nCan only add while trade is placed"
                )

            elif dict_data.st_values_holder.get("is_placed") is False:
                messagebox.showinfo(
                    "Not Open",
                    "Please place a trade to add a chart"
                )

            else:
                filename = filedialog.askopenfilename(
                    initialdir=str(Path.home() / "Desktop"),
                    title="Select 1-Hour Chart",
                    filetypes=[
                        ("Image Files", "*.png *.jpg *.jpeg")
                    ]
                )

                if not filename:
                    return

                source = Path(filename)

                # Choose a persistent storage location
                if sys.platform.startswith("win"):
                    base = Path(os.environ.get("APPDATA", Path.home()))

                elif sys.platform == "darwin":
                    base = Path.home() / "Library" / "Application Support"

                else:
                    base = Path.home() / ".local" / "share"

                # Create DocKeep chart folder
                chart_folder = base / "DocKeep" / "charts"
                chart_folder.mkdir(parents=True, exist_ok=True)

                # Copy selected image into DocKeep storage
                destination = chart_folder / "1-hour-chart.png"
                with Image.open(source) as image:
                    image = image.convert("RGB")
                    image.save(destination, format="PNG")

                # Load and resize image
                with Image.open(destination) as image:
                    resized = image.resize(
                        (1000, 530),
                        getattr(Image, "Resampling", Image).LANCZOS
                    )

                    self.new_img = ImageTk.PhotoImage(resized)

                # Display image
                self.disp_1_hour.config(
                    width=1000,
                    height=530,
                    image=self.new_img,
                    text=""
                )

                # Store image path
                dict_data.placetrade_values_holder["1-hour"] = str(destination)

        except Exception as e:
            messagebox.showerror(
                "Image Error",
                f"Failed to load the image:\n\n{type(e).__name__}: {e}"
            )

            print("1-hour chart loading error:", repr(e))

    # clears and removes a 1 hour chart
    def clear_chart(self):
        self.disp_1_hour.config(image="", text="This Chart Is Currently Empty \nClick 'Add 1-hour Chart' To Add One", width=135, height=33)
        
        dict_data.placetrade_values_holder["1-hour"] = ""

        dict_data.filetrade = open(data_path("ft_data"), "rb")
        dict_data.get_filedict_data = pickle.load(dict_data.filetrade)

        start_vars = open(data_path("startup_vars"), "rb")
        dict_data.get_dict_data = pickle.load(start_vars)
        
        dict_data.startup_load_values_to_startup()
        dict_data.st_values_holder["1-hour"] = ""

        dict_data.fileload_values_to_filedata()
        dict_data.ft_data["1-hour"] = ""

        dict_data.filetrade = open(data_path("ft_data"), "wb")
        pickle.dump(dict_data.ft_data, dict_data.filetrade)
        dict_data.filetrade.close()

        with open(data_path("startup_vars"), "wb") as start_up:
            pickle.dump(dict_data.st_values_holder, start_up)