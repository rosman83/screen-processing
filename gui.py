import os
import re
import tkinter
from tkinter import (
    Listbox,
    StringVar,
    ttk,
    Text,
    font as tkFont,
    filedialog,
    Scale,
    IntVar,
    messagebox,
)
import sv_ttk
import counts
import config
import process


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
    root.tabbar.add(screen_processing_tab, text="STEP 1")
    CreateScreenProcessingDisplay(root, screen_processing_tab)

    count_marking_tab = ttk.Frame(root.tabbar)
    root.tabbar.add(count_marking_tab, text="STEP 2")
    CreateContentMarkingDisplay(root, count_marking_tab)

    root.tabbar.pack(fill=tkinter.BOTH, expand=True)

    # init ui
    sv_ttk.set_theme("light")
    root.mainloop()


def CreateScreenProcessingDisplay(root, tab):
    # screen processing tab content
    tab.frame = ttk.Frame(tab)
    tab.frame.pack(pady=0, padx=0, fill=tkinter.BOTH, expand=True)

    # right panel - information on how to use
    tab.frame_right = ttk.Frame(tab.frame, style="Card.TFrame", padding=(5, 6, 7, 8))
    # add an outline
    tab.frame_right.config(relief=tkinter.RIDGE, borderwidth=2)
    tab.frame_right.pack(
        side=tkinter.RIGHT, pady=10, padx=5, fill=tkinter.BOTH, expand=True
    )

    tab.text = RichText(tab.frame_right, height=15, width=40)
    tab.text.pack(fill=tkinter.BOTH, expand=True)

    # right panel - information - title
    tab.text.insert("end", "Pipeline Information\n", "h1")
    tab.text.insert("end", "https://github.com/mhorlbeck/ScreenProcessing\n", "bold")
    tab.text.insert("end", "\n")
    tab.text.insert(
        "end",
        "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like) \n\n",
    )

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
    tab.frame_left = ttk.Frame(tab.frame, style="Card.TFrame", padding=(5, 6, 7, 8))
    tab.frame_left.pack(
        side=tkinter.LEFT, pady=10, padx=5, fill=tkinter.BOTH, expand=True
    )
    tab.frame_left.config(relief=tkinter.RIDGE, borderwidth=2)
    tab.frame_left.grid_columnconfigure(0, weight=1)
    tab.frame_left.title = ttk.Label(tab.frame_left, text="Parameters")
    tab.frame_left.title.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)

    # left panel - controls - parameter buttons
    # TODO: Remove this in prod...
    # fasta_file_path = None
    fasta_file_path = "/Users/rashid/Documents/Scripts/screen-processing/demo/data/CRISPRi_v1_human.trim_1_35.fa"
    # out_file_path = None
    out_file_path = "/Users/rashid/Documents/Scripts/screen-processing/demo/output"
    # seq_file_names = None
    seq_file_names = (
        "/Users/rashid/Documents/Scripts/screen-processing/demo/data/Sequencing_files/Demo_index6.fastq",
        "/Users/rashid/Documents/Scripts/screen-processing/demo/data/Sequencing_files/Demo_index3.fastq",
        "/Users/rashid/Documents/Scripts/screen-processing/demo/data/Sequencing_files/Demo_index14.fastq",
        "/Users/rashid/Documents/Scripts/screen-processing/demo/data/Sequencing_files/Demo_index12.fastq",
        "/Users/rashid/Documents/Scripts/screen-processing/demo/data/Sequencing_files/Demo_index10.fastq",
        "/Users/rashid/Documents/Scripts/screen-processing/demo/data/Sequencing_files/Demo_index1.fastq",
    )
    test_mode = False
    trim_start = IntVar(value=1)
    trim_end = IntVar(value=35)
    experiment_type = StringVar()

    def check_params(fasta_file_path, out_file_path, seq_file_names):
        if fasta_file_path is None or out_file_path is None or seq_file_names is None:
            tab.frame_left.button_submit.config(
                style="Accent.TButton", state=tkinter.DISABLED, command=None
            )
        else:
            tab.frame_left.button_submit.config(
                style="Accent.TButton", state=tkinter.NORMAL, command=start_analysis
            )

    def open_library_fasta():
        global fasta_file_path, out_file_path, seq_file_names
        button = tab.frame_left.button_library_fasta
        file_path = filedialog.askopenfilename(
            filetypes=[("Fasta Files", "*.fasta"), ("Fasta Files", "*.fa")]
        ).strip()
        print(file_path)
        if file_path is not None and file_path != "":
            fasta_file_path = file_path
            if button.cget("text") != "✓ Library_Fasta":
                button.config(text="✓ " + button.cget("text"))
            check_params(fasta_file_path, out_file_path, seq_file_names)

    def set_out_file_path():
        global fasta_file_path, out_file_path, seq_file_names
        button = tab.frame_left.button_out_file_path
        file_path = filedialog.askdirectory().strip()
        print(file_path)
        if file_path is not None and file_path != "":
            out_file_path = file_path
            if button.cget("text") != "✓ Out_File_Path":
                button.config(text="✓ " + button.cget("text"))
            check_params(fasta_file_path, out_file_path, seq_file_names)

    def set_seq_file_names():
        global fasta_file_path, out_file_path, seq_file_names
        button = tab.frame_left.button_seq_file_name
        file_path = filedialog.askopenfilenames(filetypes=[("FastQ Files", "*.fastq")])
        print(file_path)
        if file_path is not None and file_path != "":
            seq_file_names = file_path
        if button.cget("text") != "✓ Seq_File_Name":
            button.config(text="✓ " + button.cget("text"))
        check_params(fasta_file_path, out_file_path, seq_file_names)

    def start_analysis():
        args = {
            "Seq_Files_Names": seq_file_names,
            "Library_Fasta": fasta_file_path,
            "Out_File_Path": out_file_path,
            "test": test_mode,
            "trim_start": trim_start.get(),
            "trim_end": trim_end.get(),
            "experiment_type": experiment_type.get(),
        }
        # initial counts
        counts.counts_main(args)
        # TODO: Moving this to step 2 instead in marking.
        # create config TODO: Finish this
        # config.create_config(args["Out_File_Path"], args["experiment_type"])
        # process experiment
        # process.processExperimentsFromConfig(args["library_tables_file_path"])

    tab.frame_left.button_library_fasta = ttk.Button(
        tab.frame_left, text="Upload Fasta Library File", command=open_library_fasta
    )
    tab.frame_left.button_library_fasta.grid(
        row=2, column=0, sticky="nsew", pady=(15, 5), columnspan=2
    )

    tab.frame_left.button_seq_file_name = ttk.Button(
        tab.frame_left,
        text="Upload Sequencing file(s)",
        command=set_seq_file_names,
    )
    tab.frame_left.button_seq_file_name.grid(
        row=3, column=0, sticky="nsew", pady=5, columnspan=2
    )

    tab.frame_left.button_out_file_path = ttk.Button(
        tab.frame_left, text="Set Output Directory", command=set_out_file_path
    )
    tab.frame_left.button_out_file_path.grid(
        row=5, column=0, sticky="nsew", pady=5, columnspan=2
    )

    # create label for trim_start and trim_end

    tab.frame_left.trim_start = Scale(
        tab.frame_left, from_=1, orient=tkinter.HORIZONTAL, variable=trim_start
    )
    tab.frame_left.trim_start.grid(row=6, column=1, sticky="nsew", pady=5)
    tab.frame_left.trim_start_label = ttk.Label(
        tab.frame_left, text=("Trim Start Value")
    )
    tab.frame_left.trim_start_label.grid(row=6, column=0, sticky="nsew", pady=5)

    tab.frame_left.trim_end = Scale(
        tab.frame_left, from_=1, orient=tkinter.HORIZONTAL, variable=trim_end
    )
    tab.frame_left.trim_end.grid(row=7, column=1, sticky="nsew", pady=5)
    tab.frame_left.trim_end_label = ttk.Label(tab.frame_left, text="Trim End Value")
    tab.frame_left.trim_end_label.grid(row=7, column=0, sticky="nsew", pady=5)

    tab.frame_left.test_mode_toggle = ttk.Checkbutton(
        tab.frame_left,
        style="Switch.TCheckbutton",
        text="Run in test mode",
        variable=test_mode,
        onvalue=True,
        offvalue=False,
    )
    tab.frame_left.test_mode_toggle.grid(
        row=8, column=0, sticky="nsew", pady=10, columnspan=2
    )

    tab.frame_left.button_submit = ttk.Button(tab.frame_left, text="Start Analysis")
    # prod: tab.frame_left.button_submit.config(style="Accent.TButton", state=tkinter.DISABLED, command=start_analysis)
    tab.frame_left.button_submit.config(
        style="Accent.TButton", state=tkinter.NORMAL, command=start_analysis
    )

    tab.frame_left.button_submit.grid(row=9, column=0, sticky="nsew", columnspan=2)

def CreateContentMarkingDisplay(root, tab):
    # vars
    experiment_type_options = [
        "CRISPRi_v2_human",
        "CRISPRa_v2_human",
        "CRISPRi_v2_mouse",
        "CRISPRa_v2_mouse",
        "CRISPRi_v1",
        "CRISPRa_v1",
    ]
    
    experiment_type = StringVar()
    folder_path = None
    counts_files = None
    counts_files_obj = None
    library_tables_file_path = None
    # folder_path = '/Users/rashid/Documents/Scripts/screen-processing/demo/output/count_files'
    # counts_files = ['Demo_index14_CRISPRi_v1_human.trim_1_35.fa.counts', 'Demo_index1_CRISPRi_v1_human.trim_1_35.fa.counts', 'Demo_index6_CRISPRi_v1_human.trim_1_35.fa.counts', 'Demo_index12_CRISPRi_v1_human.trim_1_35.fa.counts', 'Demo_index10_CRISPRi_v1_human.trim_1_35.fa.counts', 'Demo_index3_CRISPRi_v1_human.trim_1_35.fa.counts']

    # content marking tab content
    tab.frame = ttk.Frame(tab)
    tab.frame.pack(pady=0, padx=0, fill=tkinter.BOTH, expand=True)

    # left panel - controls for screen processing
    tab.frame_left = ttk.Frame(tab.frame, style="Card.TFrame", padding=(5, 6, 7, 8))
    tab.frame_left.pack(
        side=tkinter.LEFT, pady=10, padx=5, fill=tkinter.BOTH, expand=True
    )
    tab.frame_left.config(relief=tkinter.RIDGE, borderwidth=2)
    tab.frame_left.grid_columnconfigure(0, weight=1)
    tab.frame_left.title = ttk.Label(tab.frame_left, text="Parameters")
    tab.frame_left.title.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)

    def set_directory_file_path():
        global folder_path, counts_files, counts_files_obj
        temp_folder_path = filedialog.askdirectory().strip()
        if temp_folder_path is not None and temp_folder_path != "":
            folder_path = temp_folder_path
            counts_files = None
            counts_files_obj = []
            scan_directory_file_path()

    def scan_directory_file_path():
        global folder_path, counts_files, counts_files_obj
        counts_files = [
            fileName
            for fileName in os.listdir(folder_path)
            if fileName.endswith(".counts")
        ]
        counts_files.sort(key=lambda f: int(re.sub("\D", "", f)))
        for file_name in counts_files:
            counts_files_obj.append(
                {
                    "file_name": file_name,
                    "path": folder_path + "/" + file_name,
                    "condition": "",
                    "replicate_id": "",
                }
            )
        counts_files_obj.sort(key=lambda f: int(re.sub("\D", "", f["file_name"])))
        render_counts_files()

    # Create an input ttk box to enter experiment type
    # options are CRISPRi_v2_human, CRISPRa_v2_human, CRISPRi_v2_mouse, CRISPRa_v2_mouse, CRISPRi_v1, CRISPRa_v1
    tab.frame_left.label_experiment_type = ttk.OptionMenu(
        tab.frame_left,
        experiment_type,
        experiment_type_options[0],
        *experiment_type_options,
    )
    tab.frame_left.label_experiment_type.grid(
        row=1, column=0, sticky="nsew", pady=5, padx=5, columnspan=2
    )

    # get library table
    def set_library_tables_file_path():
        global library_tables_file_path
        file_path = filedialog.askdirectory().strip()
        if file_path is not None and file_path != "":
            library_tables_file_path = file_path

    tab.frame_left.button_library_tables_file_path = ttk.Button(
        tab.frame_left,
        text="Set Library Tables Directory",
        command=set_library_tables_file_path,
    )
    tab.frame_left.button_library_tables_file_path.grid(
        row=2, column=0, sticky="nsew", pady=5, columnspan=2
    )

    def submit_counts_files():
        # create config
        global counts_files_obj, folder_path, library_tables_file_path
        config.create_config(folder_path, experiment_type.get(), counts_files_obj)

        # process experiment
        process.processExperimentsFromConfig(library_tables_file_path)
        return

    # initial upload button
    tab.frame_left.button_upload = ttk.Button(
        tab.frame_left, text="Select Counts Folder"
    )
    tab.frame_left.button_upload.config(
        style="Accent.TButton", state=tkinter.NORMAL, command=set_directory_file_path
    )
    tab.frame_left.button_upload.grid(row=3, column=0, sticky="nsew", columnspan=2)

    # conditional display: if counts_files is not None, display the files, allow user to mark them as control or not

    ttk.Separator(tab.frame_left, orient=tkinter.HORIZONTAL).grid(
        row=4, column=0, sticky="nsew", pady=5, padx=5, columnspan=2
    )

    tab.frame_left.label_counts_files = ttk.Label(
        tab.frame_left,
        text="Uploaded Counts Files\n\nPlease input the [condition] and [replicate_id] in the respective columns.\nexample: [file index 1] | untreated | replicate_1",
    )
    tab.frame_left.label_counts_files.grid(
        row=5, column=0, sticky="nsew", pady=5, padx=5, columnspan=2
    )

    def render_counts_files():
        global counts_files, counts_files_obj
        if counts_files_obj is not None and len(counts_files_obj) > 0:
            # create a vertical list of rows, each row has three input boxes, with the first being the file name and disabled, and the other two blank
            tab.frame_left.list_count_files = ttk.Frame(tab.frame_left)
            tab.frame_left.list_count_files.grid(
                row=6,
                column=0,
                sticky="nsew",
                pady=5,
                padx=5,
                columnspan=2,
                rowspan=(len(counts_files_obj)),
            )

            for idx, obj in enumerate(counts_files_obj):
                # TODO: Create a stack trace and make the variables stringvars to link here..
                # good luck with this..
                condition = StringVar()
                replicate_id = StringVar()
                # create a stack trace for the condition and replicate_id variables from the respective object, whenever condition or replicate_id is updated, update the object
                condition.trace(
                    "w",
                    lambda name, index, mode, sv=condition, obj=obj: obj.__setitem__(
                        "condition", sv.get()
                    ),
                )
                replicate_id.trace(
                    "w",
                    lambda name, index, mode, sv=replicate_id, obj=obj: obj.__setitem__(
                        "replicate_id", sv.get()
                    ),
                )

                # create a label for the specific count
                tab.frame_left.list_count_files.label_file_name = ttk.Label(
                    tab.frame_left.list_count_files, text=obj["file_name"]
                )
                tab.frame_left.list_count_files.label_file_name.grid(
                    row=(5 + idx + 1), column=0, sticky="nsew", pady=5, padx=5
                )

                tab.frame_left.list_count_files.label_condition = ttk.Entry(
                    tab.frame_left.list_count_files, width=15, textvariable=condition
                )
                tab.frame_left.list_count_files.label_condition.grid(
                    row=(5 + idx + 1), column=1, sticky="nsew", pady=5, padx=5
                )

                tab.frame_left.list_count_files.label_treatment = ttk.Entry(
                    tab.frame_left.list_count_files, width=15, textvariable=replicate_id
                )
                tab.frame_left.list_count_files.label_treatment.grid(
                    row=(5 + idx + 1), column=2, sticky="nsew", pady=5, padx=5
                )

            # create submission button
            tab.frame_left.list_count_files.button_submit = ttk.Button(
                tab.frame_left, text="Submit"
            )
            tab.frame_left.list_count_files.button_submit.config(
                style="Accent.TButton",
                state=tkinter.NORMAL,
                command=submit_counts_files,
            )
            tab.frame_left.list_count_files.button_submit.grid(
                row=(5 + len(counts_files) + 1), column=0, sticky="nsew"
            )


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
        h1_font.configure(size=int(default_size * 2), weight="bold")

        self.tag_configure("bold", font=bold_font)
        self.tag_configure("italic", font=italic_font)
        self.tag_configure("h1", font=h1_font, spacing3=default_size)

        lmargin2 = em + default_font.measure("\u2022 ")
        self.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)

    def insert_bullet(self, index, text):
        self.insert(index, f"\u2022 {text}", "bullet")
