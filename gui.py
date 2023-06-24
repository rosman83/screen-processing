import tkinter
from tkinter import ttk, Text, font as tkFont, filedialog
import sv_ttk


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
    root.tabbar.add(screen_processing_tab, text="Screen Processing")
    root.tabbar.pack(fill=tkinter.BOTH, expand=True)
    
    # tab content
    CreateScreenProcessingDisplay(screen_processing_tab)
    
    # init ui
    sv_ttk.set_theme("light")
    root.mainloop()
        
def CreateScreenProcessingDisplay(tab):
    # screen processing tab content
    tab.frame = ttk.Frame(tab)
    tab.frame.pack(pady=0, padx=0, fill=tkinter.BOTH, expand=True)
    
    # right panel - information on how to use
    tab.frame_right = ttk.Frame(tab.frame)
    # add an outline
    tab.frame_right.config(relief=tkinter.RIDGE, borderwidth=2)
    tab.frame_right.pack(side=tkinter.RIGHT, pady=10, padx=5, fill=tkinter.BOTH, expand=True)

    tab.text = RichText(tab.frame_right, height=15, width=40)
    tab.text.pack(fill=tkinter.BOTH, expand=True)
    
    # right panel - information - title
    tab.text.insert("end", "Pipeline Information\n", "h1")
    tab.text.insert("end", "https://github.com/mhorlbeck/ScreenProcessing\n", "bold")
    tab.text.insert("end", "\n")
    tab.text.insert("end", "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like) \n\n")
    
    # right panel - information - params table
    tab.text.insert_bullet("end", "")
    tab.text.insert("end", "Library_Fasta: ", "bold")
    tab.text.insert("end", "Fasta file of expected library reads.\n")
    tab.text.insert_bullet("end", "")
    tab.text.insert("end", "Out_File_Path: ", "bold")
    tab.text.insert("end", "Directory where output files should be written.\n")
    tab.text.insert_bullet("end", "")
    tab.text.insert("end", "Seq_File_Name: ", "bold")
    tab.text.insert("end", "Name(s) of sequencing file(s).\n")
    
    # left panel - controls for screen processing
    tab.frame_left = ttk.Frame(tab.frame)
    tab.frame_left.pack(side=tkinter.LEFT, pady=10, padx=5, fill=tkinter.BOTH, expand=True)
    tab.frame_left.config(relief=tkinter.RIDGE, borderwidth=2)
    tab.frame_left.grid_columnconfigure(0, weight=1)
    tab.frame_left.title = ttk.Label(tab.frame_left, text="Screen Processing")
    tab.frame_left.title.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)
    
    # left panel - controls - parameter buttons
    def open_library_fasta():
        button = tab.frame_left.button_library_fasta
        file_path = filedialog.askopenfilename()
        #TODO: add checks for valid file
        button.config(text="✓ " + button.cget("text"))
        
    tab.frame_left.button_library_fasta = ttk.Button(tab.frame_left, text="Library_Fasta", command=open_library_fasta)
    tab.frame_left.button_library_fasta.grid(row=1, column=0, sticky="nsew")
    
    tab.frame_left.button_out_file_path = ttk.Button(tab.frame_left, text="Out_File_Path", command=lambda: print("Out_File_Path"))
    tab.frame_left.button_out_file_path.grid(row=2, column=0, sticky="nsew")
    
    tab.frame_left.button_seq_file_name = ttk.Button(tab.frame_left, text="Seq_File_Name", command=lambda: print("Seq_File_Name"))
    tab.frame_left.button_seq_file_name.grid(row=3, column=0, sticky="nsew")
    
class RichText(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_font = tkFont.nametofont(self.cget("font"))

        em = default_font.measure("m")
        default_size = default_font.cget("size")
        bold_font = tkFont.Font(**default_font.configure())
        italic_font = tkFont.Font(**default_font.configure())
        h1_font = tkFont.Font(**default_font.configure())

        bold_font.configure(weight="bold")
        italic_font.configure(slant="italic")
        h1_font.configure(size=int(default_size*2), weight="bold")

        self.tag_configure("bold", font=bold_font)
        self.tag_configure("italic", font=italic_font)
        self.tag_configure("h1", font=h1_font, spacing3=default_size)

        lmargin2 = em + default_font.measure("\u2022 ")
        self.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)

    def insert_bullet(self, index, text):
        self.insert(index, f"\u2022 {text}", "bullet")
    