import tkinter
from tkinter import (
    ttk,
)
import sv_ttk

import gui.counts_gui as counts_gui
import gui.process_gui as process_gui
import gui.settings_gui as settings_gui

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
