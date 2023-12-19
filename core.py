from multiprocessing import freeze_support
import config

# TODO: Test with exact environment python vers/lib vers
# TODO: Look into interactive python stuff...
# TODO: Setup compilation support

if __name__ == '__main__':
  freeze_support()
  # Initialize config
  config.init_config()
  # add dynamic config saving support
  # root.protocol("WM_DELETE_WINDOW", saveConfig)
  # Create display 
  
  from gui.display_gui import CreateDisplay
  CreateDisplay()