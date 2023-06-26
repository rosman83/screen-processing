import shutil
import random
import fileinput


def create_config(output_folder, library):
    # Step 1: Create a copy of the default experiment config file
    shutil.copyfile("experiment_config_file_BLANK.txt", "experiment_config_file.txt")
    random_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))

    # Step 2: Append output_folder to line 4
    with fileinput.FileInput("experiment_config_file.txt", inplace=True) as file:
        for line_number, line in enumerate(file, start=1):
            if line_number == 6:
                line = line.rstrip() + " " + output_folder + "\n"
            if line_number == 7:
                line = line.rstrip() + " " + random_id + "\n"
            if line_number == 15:
                line = line.rstrip() + " " + library + "\n"
            print(line, end='')
