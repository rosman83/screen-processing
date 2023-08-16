import os
import re
import tkinter
from tkinter import (
    StringVar,
    ttk,
    filedialog,
    Scale,
    IntVar,
    Text,
    font as tkFont,
)
import config
import process

def process_gui_init(root, tab):
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
