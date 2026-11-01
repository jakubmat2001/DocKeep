import os
import shutil
import sys
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
import pickle
import tkinter as tk
import retrivables.dict_data as dict_data
from retrivables.helpers import data_path

# various fonts used for label widgets
App_font = ("Sans-Serif", 13)
Body_font = ("Sans-Serif", 9)

# a fifteen min tab which holds some of the opeartions for uploading 15-min charts
class fifteen_min(tk.Frame):
    def __init__(self, parent, controller):
        import pages.mainpage_raised as mainpage_raised ,pages.four_hour_raised as four_hour_raised, pages.one_hour_raised as one_hour_raised, retrivables.result_raised as result_raised
        tk.Frame.__init__(self, parent)

        self.test_img = ""
        self.resizingImg = ""
        self.new_img = ""

        self.tabs_bar = tk.Frame(self, bg="#DC7979", width=110)
        self.tabs_bar.grid(row=0, column=0, sticky="we")

        self.fifteen_body = tk.Frame(self, bg="#FDFDFD", padx=20, pady=20)
        self.fifteen_body.grid(row=2, column=0, sticky="nsew")

        self.banner_lbl = tk.Label(self, text="15 Min",font=App_font ,width=110, height=5, bg="#BDBABA")
        self.banner_lbl.grid(row=1, column=0, sticky="we" )

        self.button16 = tk.Button(self.tabs_bar, text="Main", command=lambda: controller.show_frame(mainpage_raised.mainpage), justify="center", 
                                pady=3, borderwidth=1, relief="groove")
        self.button16.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

        self.button17 = tk.Button(self.tabs_bar, text="4 Hour", command=lambda: controller.show_frame(four_hour_raised.four_hour), justify="center", 
                                pady=3, borderwidth=1, relief="groove")
        self.button17.grid(row=0, column=2, padx=(5, 5), pady=(5, 5))

        self.button18 = tk.Button(self.tabs_bar, text="1 Hour", command=lambda: controller.show_frame(one_hour_raised.one_hour), justify="center", 
                                pady=3, borderwidth=1, relief="groove")
        self.button18.grid(row=0, column=3, padx=(5, 5), pady=(5, 5))

        self.button19 = tk.Button(self.tabs_bar, text="15 Min", command=lambda: controller.show_frame(fifteen_min), justify="center", 
                                pady=3, borderwidth=1, relief="groove")
        self.button19.grid(row=0, column=4, padx=(5, 5), pady=(5, 5))

        self.button20 = tk.Button(self.tabs_bar, text="Result", command=lambda: controller.show_frame(result_raised.result), justify="center", 
                                pady=3, borderwidth=1, relief="groove")
        self.button20.grid(row=0, column=5, padx=(5, 5), pady=(5, 5))

        self.disp_15_min = tk.Label(self.fifteen_body, width=110, height=33, image=self.test_img, text="This Chart Is Currently Empty \nClick 'Add 15-Min Chart' To Add One" ,relief="solid", borderwidth=1)
        self.disp_15_min.grid(rowspan=20, columnspan=5)

        self.fif_min_button = tk.Button(self.fifteen_body, text="Add 15-min\nChart" ,command=lambda: fifteen_min.add_15_min(self), justify="center")
        self.fif_min_button.grid(row=10, column=5, padx=(20, 0))

        self.clear_15_min = tk.Button(self.fifteen_body, text="Clear\nChart", command=lambda: fifteen_min.clear_chart(self))
        self.clear_15_min.grid(row=11, column=5, padx=(20, 0))

        # places added chart on a label if it was uploaded in the past
        def get_img(self):
            try:
                if dict_data.st_values_holder.get("is_placed") is True:
                    image_path = dict_data.placetrade_values_holder.get("15-min")
                else:
                    with open(data_path("ft_data"), "rb") as filetrade:
                        dict_data.get_filedict_data = pickle.load(filetrade)

                    image_path = dict_data.get_filedict_data.get("15-min")

                if not image_path:
                    return

                with Image.open(image_path) as image:
                    resized = image.resize(
                        (1000, 530),
                        getattr(Image, "Resampling", Image).LANCZOS
                    )

                    self.new_img = ImageTk.PhotoImage(resized)

                self.disp_15_min.config(
                    width=1000,
                    height=530,
                    image=self.new_img,
                    text=""
                )

            except Exception as e:
                print("15-minute chart loading error:", repr(e))


        get_img(self)

    # adds a 15 minute chart selected by a user
    def add_15_min(self):
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
                    title="Select 15-Minute Chart",
                    filetypes=[
                        ("Image Files", "*.png *.jpg *.jpeg")
                    ]
                )

                if not filename:
                    return

                source = Path(filename)

                # Choose persistent storage location
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
                destination = chart_folder / "15-min-chart.png"
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
                self.disp_15_min.config(
                    width=1000,
                    height=530,
                    image=self.new_img,
                    text=""
                )

                # Store image path
                dict_data.placetrade_values_holder["15-min"] = str(destination)

        except Exception as e:
            messagebox.showerror(
                "Image Error",
                f"Failed to load the image:\n\n{type(e).__name__}: {e}"
            )

            print("15-minute chart loading error:", repr(e))
    
    # clears and removes a fifteen min charts
    def clear_chart(self):
        self.disp_15_min.config(image="", text="This Chart Is Currently Empty \nClick 'Add 15-min Chart' To Add One", width=135, height=33)
        
        dict_data.placetrade_values_holder["15-min"] = ""

        dict_data.filetrade = open(data_path("ft_data"), "rb")
        dict_data.get_filedict_data = pickle.load(dict_data.filetrade)

        start_vars = open(data_path("startup_vars"), "rb")
        dict_data.get_dict_data = pickle.load(start_vars)

        dict_data.startup_load_values_to_startup()
        dict_data.st_values_holder["15-min"] = ""

        dict_data.fileload_values_to_filedata()
        dict_data.ft_data["15-min"] = ""

        dict_data.filetrade = open(data_path("ft_data"), "wb")
        pickle.dump(dict_data.ft_data, dict_data.filetrade)
        dict_data.filetrade.close()
        
        with open(data_path("startup_vars"), "wb") as start_up:
            pickle.dump(dict_data.st_values_holder, start_up)