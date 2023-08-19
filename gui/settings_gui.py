import tkinter
from tkinter import IntVar, StringVar, Tk, ttk, BooleanVar, DoubleVar
from configparser import ConfigParser

import gui.display_gui as display_gui

def settings_gui_init(root, tab):
  # global variables
  config = ConfigParser()
  config.read('config.ini')
  filter_type = StringVar(value=config.get('filter_settings', 'filter_type'))
  minimum_reads = IntVar(value=config.getint('filter_settings', 'minimum_reads'))
  condition_string = StringVar(value=config.get('sgrna_analysis', 'condition_string'))
  pseudocount_behavior = StringVar(value=config.get('sgrna_analysis', 'pseudocount_behavior'))
  pseudocount = DoubleVar(value=config.getfloat('sgrna_analysis', 'pseudocount'))
  collapse_to_transcripts = BooleanVar(value=config.getboolean('gene_analysis', 'collapse_to_transcripts'))
  generate_pseudogene_dist = StringVar(value=config.get('gene_analysis', 'generate_pseudogene_dist'))
  pseudogene_size = IntVar(value=config.getint('gene_analysis', 'pseudogene_size'))
  num_pseudogenes = IntVar(value=config.getint('gene_analysis', 'num_pseudogenes'))
  calculate_ave = BooleanVar(value=config.getboolean('gene_analysis', 'calculate_ave'))
  best_n = IntVar(value=config.getint('gene_analysis', 'best_n'))
  calculate_mw = BooleanVar(value=config.getboolean('gene_analysis', 'calculate_mw'))
  calculate_nth = BooleanVar(value=config.getboolean('gene_analysis', 'calculate_nth'))
  nth = IntVar(value=config.getint('gene_analysis', 'nth'))
  
  # main settings panel
  tab.frame = display_gui.VerticalScrolledFrame(tab)
  tab.frame.pack(pady=0, padx=0, fill=tkinter.BOTH, expand=True)
  
  # func defs
  def filter_settings_panel(tab):
    # create a frame for the filter settings
    tab.filter_settings_frame = ttk.Frame(tab.frame.interior, style="Card.TFrame", padding=(5, 6, 7, 8))
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
    
    filter_type_combobox = ttk.Combobox(tab.filter_settings_frame, textvariable=filter_type, values=["either", "both"])
    filter_type_combobox.grid(row=2, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
    # create a control to edit minimum_reads, being an integer
    minimum_reads_label = ttk.Label(tab.filter_settings_frame, text="Minimum Reads")
    minimum_reads_label.grid(row=3, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    minimum_reads_entry = ttk.Entry(tab.filter_settings_frame, textvariable=minimum_reads)
    minimum_reads_entry.grid(row=3, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
  def sgrna_analysis_settings_panel(tab):
    # create a frame for the sgrna_analysis settings
    tab.sgrna_analysis_settings_frame = ttk.Frame(tab.frame.interior, style="Card.TFrame", padding=(5, 6, 7, 8))
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
    def update_var_from_textbox():
      condition_string.set(sgrna_analysis_conditions_entry.get("1.0", tkinter.END))
    sgrna_analysis_conditions_entry = tkinter.Text(tab.sgrna_analysis_settings_frame, height=10, width=50)
    sgrna_analysis_conditions_entry.insert(tkinter.END, condition_string.get())
    sgrna_analysis_conditions_entry.bind('<KeyRelease>',lambda *args: update_var_from_textbox())
    sgrna_analysis_conditions_entry.grid(row=1, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
  def possible_treatment_settings_panel(tab):
    # create a frame for the possible_treatment settings
    tab.possible_treatment_settings_frame = ttk.Frame(tab.frame.interior, style="Card.TFrame", padding=(5, 6, 7, 8))
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
    pseudocount_behavior_combobox = ttk.Combobox(tab.possible_treatment_settings_frame, textvariable=pseudocount_behavior, values=["zeros only", "all values", "filter out"])
    pseudocount_behavior_combobox.grid(row=2, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
    # create a control to edit pseudocount, being an integer, default is 1
    pseudocount_label = ttk.Label(tab.possible_treatment_settings_frame, text="Pseudocount")
    pseudocount_label.grid(row=3, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    pseudocount_entry = ttk.Entry(tab.possible_treatment_settings_frame, textvariable=pseudocount)
    pseudocount_entry.grid(row=3, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
  def gene_analysis_settings_panel(tab):
    # create a frame for the gene_analysis settings
    tab.gene_analysis_settings_frame = ttk.Frame(tab.frame.interior, style="Card.TFrame", padding=(5, 6, 7, 8))
    tab.gene_analysis_settings_frame.pack(
      pady=10, padx=5, fill=tkinter.BOTH, expand=False
    )
    tab.gene_analysis_settings_frame.config(relief=tkinter.RIDGE, borderwidth=2)
    tab.gene_analysis_settings_frame.grid_columnconfigure(0, weight=1)
    # create the introductory title and text for the gene_analysis settings
    gene_analysis_settings_title = ttk.Label(
      tab.gene_analysis_settings_frame,
      text="Gene Analysis Settings",
      font=('Helvetica', 16, 'bold')
    )
    gene_analysis_settings_title.grid(row=0, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    # create a control to toggle collapse_to_transcripts being either True or False, default is True with a label in the same row
    collapse_to_transcripts_label = ttk.Label(
      tab.gene_analysis_settings_frame,
      text="Collapse to Transcripts",
    )
    collapse_to_transcripts_label.grid(row=1, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    collapse_to_transcripts_checkbutton = ttk.Checkbutton(tab.gene_analysis_settings_frame, variable=collapse_to_transcripts, style="Switch.TCheckbutton")
    collapse_to_transcripts_checkbutton.grid(row=1, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
    # create a description for collapse_to_transcripts under that control in the row under it
    collapse_to_transcripts_description = ttk.Label(
      tab.gene_analysis_settings_frame,
      text="Set to true to combine sgRNAs by transcripts, false to combine by genes. If this is set to true and calculate Mann-Whitney p-value \nis set to true, the script will also generate a table of gene scores based on the transcript with the best mw p-value",
      font=(12)
    )
    collapse_to_transcripts_description.grid(row=2, column=0, sticky="ew", columnspan=2, pady=5, padx=5)
    # create a control to change generate_pseudogene_dist from a list of options, "auto", "manual", "off", default is auto
    generate_pseudogene_dist_label = ttk.Label(
      tab.gene_analysis_settings_frame,
      text="Generate Pseudogene Distribution",
    )
    generate_pseudogene_dist_label.grid(row=3, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    generate_pseudogene_dist_combobox = ttk.Combobox(tab.gene_analysis_settings_frame, textvariable=generate_pseudogene_dist, values=["auto", "manual", "off"])
    generate_pseudogene_dist_combobox.grid(row=3, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
    # create a description for generate_pseudogene_dist under that control in the row under it
    generate_pseudogene_dist_description = ttk.Label(
      tab.gene_analysis_settings_frame,
      text="Generates a distribution of negative control genes by randomly sampling. \nUsed to perform same metric calculations on this set. Set to auto to match the pseudogenes with the \ntargeting library table, manual to specify pseudogenes with the below \nsettings, or off to not generate pseudogene distributions",
      font=(12),
      style="Description.TLabel"
    )
    generate_pseudogene_dist_description.grid(row=4, column=0, sticky="ew", columnspan=2, pady=5, padx=5)
    # create a control to edit pseudogene_size, being an integer, default is 10
    pseudogene_size_label = ttk.Label(tab.gene_analysis_settings_frame, text="Pseudogene Size")
    pseudogene_size_label.grid(row=5, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    pseudogene_size_entry = ttk.Entry(tab.gene_analysis_settings_frame, textvariable=pseudogene_size)
    pseudogene_size_entry.grid(row=5, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
    # create a control to edit num_pseudogenes, being an integer, default is 16000
    num_pseudogenes_label = ttk.Label(tab.gene_analysis_settings_frame, text="Number of Pseudogenes")
    num_pseudogenes_label.grid(row=6, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    num_pseudogenes_entry = ttk.Entry(tab.gene_analysis_settings_frame, textvariable=num_pseudogenes)
    num_pseudogenes_entry.grid(row=6, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
    # create a control to toggle calculate_average_mw being either True or False, default is True with a label in the same row
    calculate_average_mw_label = ttk.Label(
      tab.gene_analysis_settings_frame,
      text="Calculate Average of best n sgRNAs",
    )
    calculate_average_mw_label.grid(row=7, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    calculate_average_mw_checkbutton = ttk.Checkbutton(tab.gene_analysis_settings_frame, variable=calculate_ave, style="Switch.TCheckbutton")
    calculate_average_mw_checkbutton.grid(row=7, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
    # create a control to edit best_n, being an integer, default is 3
    best_n_label = ttk.Label(tab.gene_analysis_settings_frame, text="Best n value")
    best_n_label.grid(row=8, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    best_n_entry = ttk.Entry(tab.gene_analysis_settings_frame, textvariable=best_n)
    best_n_entry.grid(row=8, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
    # create a description for calculate_average_mw and best_n under that control in the row under it
    calculate_average_mw_description = ttk.Label(
      tab.gene_analysis_settings_frame,
      text="Set to true to perform this analysis.\nBest is defined as largest phenotype by absolute value. -1 to take average of all.",
      font=(12)
    )
    calculate_average_mw_description.grid(row=9, column=0, sticky="ew", columnspan=2, pady=5, padx=5)
    
    # create a control to toggle calculate_mw, being either True or False, default is True with a label in the same row, "Calculate Mann-Whitney p-values"
    calculate_mw_label = ttk.Label(
      tab.gene_analysis_settings_frame,
      text="Calculate Mann-Whitney p-values"
    )
    calculate_mw_label.grid(row=10, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    calculate_mw_checkbutton = ttk.Checkbutton(tab.gene_analysis_settings_frame, variable=calculate_mw, style="Switch.TCheckbutton")
    calculate_mw_checkbutton.grid(row=10, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
    # create a control to enable or disable calculate_nth with the label Score based on nth best sgRNA
    calculate_nth_label = ttk.Label(
      tab.gene_analysis_settings_frame,
      text="Score based on nth best sgRNA"
    )
    calculate_nth_label.grid(row=11, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    calculate_nth_checkbutton = ttk.Checkbutton(tab.gene_analysis_settings_frame, variable=calculate_nth, style="Switch.TCheckbutton")
    calculate_nth_checkbutton.grid(row=11, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
    # create a control to edit nth, being an integer, default is 2
    nth_label = ttk.Label(tab.gene_analysis_settings_frame, text="nth value")
    nth_label.grid(row=12, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
    nth_entry = ttk.Entry(tab.gene_analysis_settings_frame, textvariable=nth)
    nth_entry.grid(row=12, column=1, sticky="nsew",  columnspan=1, pady=5, padx=5)
  def save_settings_panel(tab, c):
    # create a row with a button to save data
    tab.save_settings_frame = ttk.Frame(tab.frame.interior, style="Card.TFrame", padding=(5, 6, 7, 8))
    tab.save_settings_frame.pack(
      pady=10, padx=5, fill=tkinter.BOTH, expand=False
    )
    tab.save_settings_frame.config(relief=tkinter.RIDGE, borderwidth=2)
    tab.save_settings_frame.grid_columnconfigure(0, weight=1)
    # create a button to save settings
    save_settings_button = ttk.Button(
      tab.save_settings_frame,
      text="Save Settings",
      command=lambda: save_settings(c),
      style="Accent.TButton"
    )
    save_settings_button.grid(row=0, column=0, sticky="nsew", columnspan=1, pady=5, padx=5)
  def save_settings(c):
    # save settings to config using self variables
    # format for saving - config.set(section,key,value)          
    c.set('filter_settings', 'filter_type', filter_type.get())
    c.set('filter_settings', 'minimum_reads', str(minimum_reads.get()))
    c.set('sgrna_analysis', 'condition_string', condition_string.get())
    c.set('sgrna_analysis', 'pseudocount_behavior', pseudocount_behavior.get())
    c.set('sgrna_analysis', 'pseudocount', str(pseudocount.get()))
    c.set('gene_analysis', 'collapse_to_transcripts', str(collapse_to_transcripts.get()))
    c.set('gene_analysis', 'generate_pseudogene_dist', generate_pseudogene_dist.get())
    c.set('gene_analysis', 'pseudogene_size', str(pseudogene_size.get()))
    c.set('gene_analysis', 'num_pseudogenes', str(num_pseudogenes.get()))
    c.set('gene_analysis', 'calculate_ave', str(calculate_ave.get()))
    c.set('gene_analysis', 'best_n', str(best_n.get()))
    c.set('gene_analysis', 'calculate_mw', str(calculate_mw.get()))
    c.set('gene_analysis', 'calculate_nth', str(calculate_nth.get()))
    c.set('gene_analysis', 'nth', str(nth.get()))

    # write to config
    with open('config.ini', 'w') as configfile:
      c.write(configfile)
    # show success message in message box
    tkinter.messagebox.showinfo("Success", "Settings saved successfully")
    return
    
      # settings funcs
  
  # fun actions
  filter_settings_panel(tab)
  sgrna_analysis_settings_panel(tab)
  possible_treatment_settings_panel(tab)
  gene_analysis_settings_panel(tab)
  save_settings_panel(tab, config)
  
  
  
  

  
  
  
  
    
    
  