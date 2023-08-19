import tkinter
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import sv_ttk

import gui.counts_gui as counts_gui
import gui.process_gui as process_gui
import gui.settings_gui as settings_gui

# TODO: Add validation for minimum/maximum value slides across all tabs ex. trim end/start
def CreateDisplay():
    # window info
    root = tkinter.Tk()
    root.title("ScreenProcessing Pipeline")
    root.geometry("800x600")
    root.resizable(width=False, height=False)

    # main frame
    root.frame_main = ttk.Frame(root)
    root.frame_main.pack(pady=0, padx=0, fill=tkinter.BOTH, expand=True)

    # tab bar
    root.tabbar = ttk.Notebook(root.frame_main)

    screen_processing_tab = ttk.Frame(root.tabbar)
    root.tabbar.add(screen_processing_tab, text="Fastqgz to Counts")
    counts_gui.counts_gui_init(root, screen_processing_tab)

    count_marking_tab = ttk.Frame(root.tabbar)
    root.tabbar.add(count_marking_tab, text="Process Experiments")
    process_gui.process_gui_init(root, count_marking_tab)
    
    settings_tab = ttk.Frame(root.tabbar)
    root.tabbar.add(settings_tab, text="Settings")
    settings_gui.settings_gui_init(root, settings_tab)

    root.tabbar.pack(fill=tkinter.BOTH, expand=True)

    # init ui
    sv_ttk.set_theme("light")
    root.mainloop()

class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, 
                                width = 200, height = 300,
                                yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command = self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = ttk.Frame(self.canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)


    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width = self.interior.winfo_reqwidth())
        
    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())