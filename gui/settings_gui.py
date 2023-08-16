import tkinter
from tkinter import ttk


def settings_gui_init(root, tab):
  # main settings panel
  tab.frame = ttk.Frame(tab)
  tab.frame.pack(pady=0, padx=0, fill=tkinter.BOTH, expand=True)
  # panel to edit filter_settings
  filter_settings_panel(tab)
  # panel to edit sgrna_analysis condition
  sgrna_analysis_settings_panel(tab)
  possible_treatment_settings_panel(tab)
  # panel to enable growth values
  # panel to edit gene_analysis
def filter_settings_panel(tab):
  # create a frame for the filter settings
  tab.filter_settings_frame = ttk.Frame(tab.frame, style="Card.TFrame", padding=(5, 6, 7, 8))
  tab.filter_settings_frame.pack(
    pady=10, padx=5, fill=tkinter.BOTH, expand=False
  )
  tab.filter_settings_frame.config(relief=tkinter.RIDGE, borderwidth=2)
  tab.filter_settings_frame.grid_columnconfigure(0, weight=1)
  # create the introductory title and text for the filter settings
  filter_settings_title = ttk.Label(
    tab.filter_settings_frame,
    text="Filter Settings",
    font = ('Helvetica', 16, 'bold')
  )
  filter_settings_title.grid(row=0, column=0, sticky="nsew", columnspan=2, pady=5, padx=5)
  filter_settings_text = ttk.Label(
    tab.filter_settings_frame,
    text="Do you require greater than or equal to the minimum reads for both experiments in a comparison or either experiment?",
    font = (12)
  )
  filter_settings_text.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=5, padx=5)
  # create a control to edit filter_type, being a either "either" or "both"
  
  filter_type_label = ttk.Label(
    tab.filter_settings_frame, 
    text="Filter Type",
  )
  filter_type_label.grid(row=2, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
  filter_type = tkinter.StringVar()
  filter_type.set("either") # replace with config
  filter_type_combobox = ttk.Combobox(tab.filter_settings_frame, textvariable=filter_type, values=["either", "both"])
  filter_type_combobox.grid(row=2, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
  # create a control to edit minimum_reads, being an integer
  minimum_reads_label = ttk.Label(tab.filter_settings_frame, text="Minimum Reads")
  minimum_reads_label.grid(row=3, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
  minimum_reads = tkinter.IntVar()  
  minimum_reads.set(50) # replace with config
  minimum_reads_entry = ttk.Entry(tab.filter_settings_frame, textvariable=minimum_reads)
  minimum_reads_entry.grid(row=3, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
def sgrna_analysis_settings_panel(tab):
  # create a frame for the sgrna_analysis settings
  tab.sgrna_analysis_settings_frame = ttk.Frame(tab.frame, style="Card.TFrame", padding=(5, 6, 7, 8))
  tab.sgrna_analysis_settings_frame.pack(
    pady=10, padx=5, fill=tkinter.BOTH, expand=False
  )
  tab.sgrna_analysis_settings_frame.config(relief=tkinter.RIDGE, borderwidth=2)
  tab.sgrna_analysis_settings_frame.grid_columnconfigure(0, weight=1)
  # create the introductory title and text for the sgrna_analysis settings
  sgrna_analysis_settings_title = ttk.Label(
    tab.sgrna_analysis_settings_frame,
    text="sgRNA Analysis Settings",
    font = ('Helvetica', 16, 'bold')
  )
  sgrna_analysis_settings_title.grid(row=0, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
  sgrna_analysis_settings_text = ttk.Label(
    tab.sgrna_analysis_settings_frame,
    text="Enter the condition(s) you want to compare in seperate lines, \nfollowing the format: comparison_name:condition1:condition2\n\nFor example:\ngamma:T0:untreated\nrho:untreated:treated\ntau:T0:treated",
    font = (12)
  )
  sgrna_analysis_settings_text.grid(row=1, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
  # create a control to edit sgrna_analysis_conditions, being a list of strings
  sgrna_analysis_conditions = tkinter.StringVar()
  sgrna_analysis_conditions.set("gamma:T0:untreated\nrho:untreated:treated\ntau:T0:treated") # replace with config
  sgrna_analysis_conditions_entry = tkinter.Text(tab.sgrna_analysis_settings_frame, height=10, width=50)
  sgrna_analysis_conditions_entry.insert(tkinter.END, sgrna_analysis_conditions.get())
  sgrna_analysis_conditions_entry.grid(row=1, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
def possible_treatment_settings_panel(tab):
  # create a frame for the possible_treatment settings
  tab.possible_treatment_settings_frame = ttk.Frame(tab.frame, style="Card.TFrame", padding=(5, 6, 7, 8))
  tab.possible_treatment_settings_frame.pack(
    pady=10, padx=5, fill=tkinter.BOTH, expand=False
  )
  tab.possible_treatment_settings_frame.config(relief=tkinter.RIDGE, borderwidth=2)
  tab.possible_treatment_settings_frame.grid_columnconfigure(0, weight=1)
  # create the introductory title and text for the possible_treatment settings
  possible_treatment_settings_title = ttk.Label(
    tab.possible_treatment_settings_frame,
    text="Possible Treatment Settings for 0 values",
    font=('Helvetica', 16, 'bold')
  )
  possible_treatment_settings_title.grid(row=0, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
  possible_treatment_settings_text = ttk.Label(
    tab.possible_treatment_settings_frame,
    text="By default, for any comparison involving a 0, add 1 to both values, leaving other values untouched.\n\nOptionally, you can choose to add the pseudocount to all values, or filter out any 0s.",
    font=(12)
  )
  # create a control to select pseudocount_behavior being either "zeros only", "all values", or "filter out", default is zeros only
  possible_treatment_settings_text.grid(row=1, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
  pseudocount_behavior_label = ttk.Label(
    tab.possible_treatment_settings_frame,
    text="Pseudocount Behavior",
  )
  pseudocount_behavior_label.grid(row=2, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
  pseudocount_behavior = tkinter.StringVar()
  pseudocount_behavior.set("zeros only") # replace with config
  pseudocount_behavior_combobox = ttk.Combobox(tab.possible_treatment_settings_frame, textvariable=pseudocount_behavior, values=["zeros only", "all values", "filter out"])
  pseudocount_behavior_combobox.grid(row=2, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
  # create a control to edit pseudocount, being an integer, default is 1
  pseudocount_label = ttk.Label(tab.possible_treatment_settings_frame, text="Pseudocount")
  pseudocount_label.grid(row=3, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
  pseudocount = tkinter.IntVar()
  pseudocount.set(1) # replace with config
  pseudocount_entry = ttk.Entry(tab.possible_treatment_settings_frame, textvariable=pseudocount)
  pseudocount_entry.grid(row=3, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
  
    
    
  