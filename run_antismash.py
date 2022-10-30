''' This module runs the program antiSMASH. For this, it requires the installation of the program antiSMASH in the specified directory for third-party programs ("thirdparty_programs"). '''


import os

import create
import names_and_paths


def run_antismash(path_of_inputfile, path_of_antismash_output_directory):
    """
    Run program antiSMASH for one given input file.

    Parameters
    ----------
    path_of_inputfile : str
        Path of one input file for antiSMASH (e.g. a .fasta file).

    Returns
    -------
    1
        If antiSMASH was successfully executed for file.
    None
        If antiSMASH fails to run, e.g. incorrect input file.

    Output folder
    -------------
    If antiSMASH was executed, a folder will be created that contains results of antiSMASH for input file.
    """
    create.create_directory_if_not_exists(path_of_antismash_output_directory) # Create an empty directory, if not existed, that will contain antiSMASH-output for input file.

    # # -----------Define path-----------------------
    path_of_antismash_runfile = names_and_paths.path_of_directory_of_thirdparty_programs + "run_antismash" # Path of the antiSMASH.
    # # -----------Define path-----------------------

    # # -----------Checkpoint: check if program antiSMASH can be found-----------
    if not os.path.exists(path_of_antismash_runfile):
        print("\n\n\n>>> Cannot find antiSMASH in directory \"" + names_and_paths.name_of_directory_of_thirdparty_programs + "\"! Please run setup again! Task terminated!")
        return 0
    # # -----------Checkpoint: check if program antiSMASH can be found-----------

    # # -----------Prepare running command-----------------------
    command = path_of_antismash_runfile + " " + path_of_inputfile + " " + path_of_antismash_output_directory + " " + "--genefinding-tool" + " " + "prodigal" # Prepare running command.
    # # -----------Prepare running command-----------------------

    # # -----------Run antiSMASH-----------------------
    os.system(command)
    # # -----------Run antiSMASH-----------------------

    return 1 # To count number of antiSMASH runs.
