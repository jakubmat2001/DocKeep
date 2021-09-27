# Program Developed And Tested By; Jakub Matusik
# Application Version; 1.2.1
# 21/09/2021

# list of libraries used in the application and their use
# tkinter; building GUI for application
# PIL; opening and resizing images
# openpyxl; opening/writing and reading execel files
# requests; using html elements and requesting data from them
# webbrowser; opening internet links
# pickle; saving/loading data from files
# pandas; creating a dataframe 

# this class will functions as a main application, displaying all of the tabs found in the application
# when user clicks on the tab he wants to move too, the frame will be raised to the top
import tkinter as tk
import mainpage_raised
import four_hour_raised
import fifteen_min_raised
import one_hour_raised
import result_raised
from result_raised import result

class dockeep(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.resizable(self, width=False, height=False)
        self.winfo_toplevel().title("Doc Keep")
        self.iconbitmap("dk_ico_logo.ico")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
 
        for f in (mainpage_raised.mainpage, four_hour_raised.four_hour, one_hour_raised.one_hour, fifteen_min_raised.fifteen_min, result_raised.result):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.config(bg="#FDFDFD")
            
        
        self.show_frame(mainpage_raised.mainpage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame_to_str = str(frame)
        frame.tkraise()
        if frame_to_str == ".!frame.!result":
            result.update_lossgain(self)

if __name__ == "__main__":
    app = dockeep()
    app.mainloop()