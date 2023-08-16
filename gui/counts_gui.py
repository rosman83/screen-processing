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
import counts


def counts_gui_init(root, tab):
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
