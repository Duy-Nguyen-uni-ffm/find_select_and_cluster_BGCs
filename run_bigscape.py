''' This module requires the installation of the program BiG-SCAPE in the specified directory for third-party programs ("thirdparty_programs") and is responsible for the execution of BiG-SCAPE by piping the running command in the Terminal. First, a temporary directory is created that contains all input file(s) for this task.
    If there already exists a folder containing results e.g. from previous runs, this module will rename the output folder until a unique name is found, then it will pipe the running command to Terminal to run BiG-SCAPE with the user-specified flags (i.e. "cutoffs" and "--mibig"), if these are given. '''


import os
import re
import shutil

import create
import names_and_paths
import side_options


def run_bigscape(inputpaths, cutoffs=False):
    """
    Run program BiGSCAPE for given input file(s).

    Parameters
    ----------
    inputpaths : str
        Path of the directory that contains all input file(s) for BiGSCAPE (also path of output directory of task 2).

    Input files
    -----------
    One or many Genbank (.gbk) files given in its input directory, each should contain only one BGC.

    Returns
    -------
    True
        If BiGSCAPE was successfully executed.
    False
        If the program BiGSCAPE could not be found in directory "thirdparty_programs" or could not be run or a BiGSCAPE-output directory already exists.

    Output folder
    -------------
    If BiGSCAPE was executed, a folder will be created that contains results of BiGSCAPE, including the file "index.html".
    """
    # # -----------Define paths-----------------------
    path_of_bigscape_runfile                = names_and_paths.path_of_directory_of_thirdparty_programs + "run_bigscape" # Path of run file of BiGSCAPE.
    path_of_output_directory_from_bigscape  = names_and_paths.path_of_directory_of_output_from_bigscape
    # # -----------Define paths-----------------------

    # # -----------Checkpoint: check if BiGSCAPE can be found and run-----------
    if os.path.exists(path_of_bigscape_runfile):
        try:
            print("\n\n\n")
            os.system(path_of_bigscape_runfile) # Test running BiGSCAPE without argument (this will only print out all available running options of BiGSCAPE).
        except:
            print("\n\n\n>>> Cannot run BiG-SCAPE CORASON! Please run setup again! Task terminated!\n\n")
            return False
    else:
        print("\n\n\n>>> Cannot find BiG-SCAPE CORASON in directory \"" + names_and_paths.name_of_directory_of_thirdparty_programs + "\"! Please run setup again! Task terminated!\n\n")
        return False
    # # -----------Checkpoint: check if BiGSCAPE can be found and run-----------

    # # -----------Create an input directory (temporary) for BiGSCAPE and copy given input files to it-----------
    path_of_input_directory_for_bigscape = create.create_directory_if_not_exists(names_and_paths.path_of_directory_of_input_for_bigscape) # Create a temporary directory that contains only input files for BiGSCAPE (contains only Genbank input files but e.g. no folders). This directory will be removed after running BiGSCAPE (to avoid size of parent directory increasing quickly).

    for path_of_inputfile in inputpaths:
        name_of_inputfile = path_of_inputfile.split("/")[-1]
        shutil.copyfile(path_of_inputfile, os.path.join(path_of_input_directory_for_bigscape, name_of_inputfile))
    # # -----------Create an input directory (temporary) for BiGSCAPE and copy given input files to it-----------

    # # -----------Checkpoint: rename output if another BiGSCAPE-output folder already exists with same path-----------------------
    if os.path.isdir(path_of_output_directory_from_bigscape) and len(os.listdir(path_of_output_directory_from_bigscape)) != 0: # In case a nonempty directory containing results (e.g. created from last run) already exists:
        if side_options.rename_output_if_name_collides == True:
            path_of_output_directory_from_bigscape = path_of_output_directory_from_bigscape.replace(names_and_paths.name_of_output_directory_from_bigscape, names_and_paths.name_of_output_directory_from_bigscape + "__renamed") # Add suffix "__renamed" to name of BiGSCAPE-output directory that will be created.
            while os.path.isdir(path_of_output_directory_from_bigscape) and len(os.listdir(path_of_output_directory_from_bigscape)) != 0:
                path_of_output_directory_from_bigscape = re.sub("__renamed/?$", "___renamed/", path_of_output_directory_from_bigscape) # Rename path of BiGSCAPE-output directory until path is unique or is an empty directory. Note: the existing directory that contains BiGSCAPE results (e.g. from last run) will not be removed.
        else:
            print("\n\n\n>>> A nonempty output directory from BiG-SCAPE CORASON already exists! Task terminated!\n\n")
            return False
    # # -----------Checkpoint: rename output if another BiGSCAPE-output folder already exists with same path-----------------------

    # # -----------Prepare running command-----------------------
    command = path_of_bigscape_runfile + " " + path_of_input_directory_for_bigscape + " " + path_of_output_directory_from_bigscape + " --include_gbk_str *" # Make command line (a string) to pipe into terminal and run BiGSCAPE. IMPORTANT: "--include_gbk_str *" in the command line allows BiGSCAPE to analyze all (.gbk) files in the input directory (so that no file will be left out).
    if cutoffs:
        command += " --cutoffs " + str(cutoffs)     # Add this flag if user has provided value(s) for the parameter "cutoffs". Otherwise, this flag will not be added and BiGSCAPE will analyze with default value c = 0.3.
    if side_options.analyze_query_BGCs_with_BGCs_from_MIBiG == True:
        command += " --mibig"                       # Add flag if to use mibig database.
    # Note: do not use if...elif... block. This would allow only one flag to be used at maximum.
    # # -----------Prepare running command-----------------------

    # # -----------Run BiGSCAPE-----------------------
    os.chdir(path_of_input_directory_for_bigscape) # IMPORTANT!!! This allows "--include_gbk_str *" in the running command ("command") to actually refer to all files of selected BGCs in this directory (i.e. BiGSCAPE will analyze all given files of selected BGCs).
    os.system(command)
    os.chdir(names_and_paths.common_path) # Change back to main/common directory e.g. for next execution of pipeline.

    shutil.rmtree(path_of_input_directory_for_bigscape) # Remove input directory, as this is no longer needed after execution of task.
    # # -----------Run BiGSCAPE-----------------------

    return True
