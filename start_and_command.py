''' This is the main program that creates the USER-INTERFACE and lets user specify task(s) to be executed (see function "Entry_Point" below). For this, the program integrates other modules and, once finished checking if their (unzipped) input is available and compatible (in the CHECKPOINTS) as well as removing/renaming
    input files with duplicate name and checking for name collision as well as preparing a unique name for the output, EXECUTES the functions in these modules that will fulfill the user-specified task(s) coordinately, or, in case the input cannot be found, prints out an error message (for debugging) and terminates the corresponding task (i.e. one of the functions "TASK_1", "TASK_2", "TASK_3"). '''


import re
import os
import time
import shutil
from   datetime import datetime
from   tabulate import tabulate

import side_options
import names_and_paths
import create
import unzip
import input_parameters
import deduplicate
import run_antismash
import analyze_and_assess
from   analyze_and_assess import delimiter_btw_data_of_genes_and_DNA_seq_of_whole_BGC, label_for_file_of_one_BGC
import make_outputfiles_and_stats
import print_to_terminal
import run_bigscape
import change_permit


# # --------------------------------------------------------------------------TASK 1 OF PIPELINE: Gene prediction with antiSMASH--------------------------------------------------------------------------

def TASK_1():
    """
    Execute task 1 (BGC prediction by antiSMASH).

    Parameters
    ----------
    None.

    Input files
    -----------
    Fasta (.fasta) file(s) (can be given as zipped files/folders).

    Returns
    -------
    None.

    Output files
    ------------
    Genbank (.gbk) file(s) of detected BGCs in given input file(s).
    """
    print("\n\n\n>>> Initiating task 1 (BGC-detection by antiSMASH)...")

    # # --------------Define paths and create directory for input and output of task---------------
    path_of_input_dir_for_task_1  = create.create_directory_if_not_exists(names_and_paths.path_of_directory_of_input_for_antismash)
    path_of_output_dir_for_task_1 = create.create_directory_if_not_exists(names_and_paths.path_of_directory_of_output_from_antismash)
    # # --------------Define paths and create directory for input and output of task---------------

    # # --------------Optional: clear antiSMASH-output directory before running antiSMASH------------------
    if side_options.clear_output_of_task_1 == True:
        shutil.rmtree(path_of_output_dir_for_task_1) # Remove whole directory of output from antiSMASH.
        create.create_directory_if_not_exists(path_of_output_dir_for_task_1) # Create directory for output from antiSMASH again.
    # # --------------Optional: clear antiSMASH-output directory before running antiSMASH------------------

    # # --------------Checkpoint: check if input directory for antiSMASH is not empty (input for this task)------------------
    if len(os.listdir(path_of_input_dir_for_task_1)) == 0:
        print("\n\n\n>>> Input directory \"" + names_and_paths.name_of_input_directory_for_antismash + "\" is empty! Task terminated!\n\n")
        print("_"*200)
        return # In case input directory for antiSMASH is empty: end execution of task.
    # # --------------Checkpoint: check if input directory for antiSMASH is not empty (input for this task)------------------

    # From here, directory that contains input file(s) for antiSMASH is not empty (i.e. input for this task is available) and proceed to the next codes:

    # # --------------Unzip all file(s)/folder(s) in input directory---------------
    unzip.unzip_all_files_and_folders_in_dir(path_of_input_dir_for_task_1)
    # # --------------Unzip all file(s)/folder(s) in input directory---------------

    # # --------------Loop through input directory and find path(s) of all input file(s) for task---------------
    inputpaths = [] # Define a list that will contain path(s) of all input file(s) for antiSMASH.

    for dir, subdirs, files in os.walk(path_of_input_dir_for_task_1, topdown=True): # "os.walk()": loop through all folders and files in directory with given path "path_of_input_dir_for_task_1". "dir": path of a certain directory found inside the directory of given path "path_of_input_dir_for_task_1", "subdirs": contains name(s) of subdirectory(-ies) in the directory "dir", "files": contains name(s) of file(s) in the directory "dir". "topdown": search from given directory with given path to its deepest file(s)/folder(s).
        for name_of_file in files: # Loop through all file(s) that can be found in directory of given path "path_of_input_dir_for_task_1", here input directory for antiSMASH.
            if not name_of_file.startswith(tuple(names_and_paths.prefixes_of_names_of_incompatible_files)) and name_of_file.endswith(tuple(names_and_paths.file_extensions_of_antismash_inputfiles)): # Checkpoint: check if file is a correct input file (e.g. a .fasta file) for antiSMASH.
                path_of_inputfile = os.path.join(dir, name_of_file)
                inputpaths.append(path_of_inputfile) # Note: a list can generally hold up to 9223372036854775807 elements. So this list can contain max. that many paths of input files.
    # # --------------Loop through input directory and find path(s) of all input file(s) for task---------------

    # # --------------Deduplicate input---------------
    deduplicate.remove_or_rename_files_with_duplicate_name(inputpaths) # Remove or rename paths in the list for antiSMASH-input files with duplicate name, which will make a list of paths of input files with unique name so that their antiSMASH-output directories, which have the same name as their input files and are created in the same directory (directory for antiSMASH-output), do not conflict in their names.
    # # --------------Deduplicate input---------------

    start_antismash_run = time.time() # Start timing gene prediction by antiSMASH.
    number_of_antismash_runs = 0 # For results report.

    # # --------------Loop through list of input file(s) and run antiSMASH for each input file---------------

    for path_of_inputfile in inputpaths:
        # # -----------Prepare path of input and output-----------------------
        name_of_inputfile                   = path_of_inputfile.split("/")[-1] # Get name of antiSMASH-input file from its path. Note: this name may contain the suffix "renamed" due to the preprocessing step previously.
        name_of_antismash_output_directory  = re.sub("|".join(names_and_paths.file_extensions_of_antismash_inputfiles), "", name_of_inputfile) # Remove file extension(s) (e.g. .fasta) from name of input file to get name of antiSMASH-output directory for input file. But the suffix "renamed" remains in the name, so that this name is unique in the antiSMASH-output directory.
        path_of_antismash_output_directory  = path_of_output_dir_for_task_1 + name_of_antismash_output_directory # Make path of antiSMASH-output directory. This path should be unique due to the preprocessing step previously.

        path_of_inputfile = re.sub("_+renamed$", "", path_of_inputfile) # Get the original, correct path of input file in case this path was modified in previous preprocessing step. Note: only omit the string "renamed" at the end of the path (i.e. in name of file).
        # # -----------Prepare path of input and output-----------------------

        # # -----------Checkpoint for name collision of output: if an antiSMASH-output directory exists with same name-----------------------
        if os.path.isdir(path_of_antismash_output_directory): # In case a directory with same name already exists in antiSMASH-output directory:
            if side_options.rename_output_if_name_collides == True: # In case name of antiSMASH-output directory is to be renamed so that input file can be analyzed:
                path_of_antismash_output_directory += "__latest_output"
                while os.path.isdir(path_of_antismash_output_directory): # In case new name for output directory is not yet unique:
                    path_of_antismash_output_directory = re.sub("__latest_output$", "___latest_output", path_of_antismash_output_directory) # Extend the underscore before "latest" in name of output directory until a unique name is found.
            else:
                continue # Skip in case name of antiSMASH-output directory is not to be renamed so that input file cannot be analyzed, e.g. when user does not want to lose old output.
        # # -----------Checkpoint for name collision of output: if an antiSMASH-output directory exists with same name-----------------------

        # # --------------Run antiSMASH for each input file---------------
        if side_options.verbose == True: print("\n\n\n>>> Running antiSMASH for file \"" + name_of_inputfile + "\"...")
        number_of_antismash_runs += run_antismash.run_antismash(path_of_inputfile, path_of_antismash_output_directory) # Run antiSMASH for input file and update the number of antiSMASH runs.
        # # --------------Run antiSMASH for each input file---------------

    end_antismash_run  = time.time() # Stop timing gene prediction by antiSMASH.
    antismash_run_time = end_antismash_run - start_antismash_run

    print("\n\n\n>>> Task 1: Finished BGC-prediction by antiSMASH for " + str(number_of_antismash_runs) + " input file(s) in directory \"" + names_and_paths.name_of_input_directory_for_antismash + "\" (antiSMASH run time = " + str(round(antismash_run_time, 1)) + " s)!\n\n")
    print("_"*200)

    # # --------------Loop through list of input file(s) and run antiSMASH for each input file---------------

# # --------------------------------------------------------------------------TASK 1 OF PIPELINE: Gene prediction with antiSMASH--------------------------------------------------------------------------


# # --------------------------------------------------------------------------TASK 2 OF PIPELINE: BGC-selection from antiSMASH-output--------------------------------------------------------------------------

def TASK_2(param_for_preliminary_selection, param_for_main_selection, param_for_2nd_chance_selection):
    """
    Execute task 2 (BGC-selection).

    Parameters
    ----------
    param_for_preliminary_selection : dict of {str : str}
        Parameter for preliminary selection, i.e. minimum number of core genes.
    param_for_main_selection : dict of {str : str}
        Parameters for main selection, i.e. minimum length of cluster (in bp), minimum distance of each core gene to edges of cluster (in bp) and minimum number of additional biosynthetic genes.
    param_for_2nd_chance_selection : dict of {str : str}
        Parameter for second-chance selection, i.e. minimum number of additional biosynthetic genes.

    Input files
    -----------
    Genbank (.gbk) file(s), each contains only one BGC (output from task 1 or can be provided externally).

    Returns
    -------
    None.

    Output files
    ------------
    Genbank (.gbk) file(s) of BGCs that passed main or second-chance selection (content unmodified compared to input file(s)).
    """
    print("\n\n\n>>> Initiating task 2 (BGC-selection)...")

    # # --------------Define paths and create directory for input and output of task---------------
    path_of_input_dir_for_task_2  = create.create_directory_if_not_exists(names_and_paths.path_of_directory_of_output_from_antismash)
    path_of_output_dir_for_task_2 = create.create_directory_if_not_exists(names_and_paths.path_of_directory_of_selected_BGCs)
    # # --------------Define paths and create directory for input and output of task---------------

    # # --------------Optional: clear directory of selected BGCs before BGC-selection------------------
    if side_options.clear_output_of_task_2 == True:
        shutil.rmtree(path_of_output_dir_for_task_2) # Remove whole directory of selected BGCs.
        create.create_directory_if_not_exists(path_of_output_dir_for_task_2) # Create directory for selected BGCs again.
    # # --------------Optional: clear directory of selected BGCs before BGC-selection------------------

    # # --------------Checkpoint: check if output directory of antiSMASH is not empty (input for this task)------------------
    if len(os.listdir(path_of_input_dir_for_task_2)) == 0:
        print("\n\n\n>>> Input directory \"" + names_and_paths.name_of_output_directory_from_antismash + "\" is empty! Task terminated!\n\n")
        print("_"*200)
        return # In case output directory for antiSMASH is empty: end execution of task.
    # # --------------Checkpoint: check if output directory of antiSMASH is not empty (input for this task)------------------

    # From here, directory that contains output file(s) for antiSMASH is not empty (i.e. input for this task is available) and proceed to the next codes:

    # # --------------Unzip all file(s)/folder(s) in input directory---------------
    unzip.unzip_all_files_and_folders_in_dir(path_of_input_dir_for_task_2)
    # # --------------Unzip all file(s)/folder(s) in input directory---------------

    # # --------------Loop through input directory and find path(s) of all input file(s) for task---------------
    inputpaths = [] # Define a list that will contain path(s) of all output file(s) of antiSMASH.

    for dir, subdirs, files in os.walk(path_of_input_dir_for_task_2, topdown=True): # "os.walk()": loop through all folders and files in directory with given path "path_of_input_dir_for_task_2". "dir": path of a certain directory found inside the directory of given path "path_of_input_dir_for_task_2", "subdirs": contains name(s) of subdirectory(-ies) in the directory "dir", "files": contains name(s) of file(s) in the directory "dir". "topdown": search from given directory with given path to its deepest file(s)/folder(s).
        for name_of_file in files: # Loop through all file(s) that can be found in directory of given path "path_of_input_dir_for_task_2", here output directory of antiSMASH.
            if not name_of_file.startswith(tuple(names_and_paths.prefixes_of_names_of_incompatible_files)) and name_of_file.endswith(tuple(names_and_paths.file_extensions_of_antismash_outputfiles)): # Checkpoint: check if file is a correct input file for task (e.g. a .gbk file), but here not yet check if file (should be .gbk file) contains only one BGC or many (this is done below).
                path_of_inputfile = os.path.join(dir, name_of_file)
                inputpaths.append(path_of_inputfile)
    # # --------------Loop through input directory and find path(s) of all input file(s) for task---------------

    # # --------------Deduplicate input---------------
    deduplicate.remove_or_rename_files_with_duplicate_name(inputpaths) # Remove or rename paths in the list of antiSMASH-output files with duplicate name, which will make a list of paths of input files each with a unique name.
    # # --------------Deduplicate input---------------

    start_analysis = time.time() # For results report.

    # # --------------Define dictionaries for statistics of BGCs (selected + discarded + all) and their products (only of selected BGCs) found in all antiSMASH-output------------------
    BGC_stats = {
    "BGCs selected"                                 : 0,
    "BGCs discarded"                                : 0,
    "All BGCs"                                      : 0
    } # Statistics of BGC-selection from all antiSMASH-output.
      # Important: selected BGCs refer to BGCs selected either by main or by second-chance selection.

    product_stats = {} # Statistics that count the product(s) of selected BGCs from all antiSMASH-output. Key = a product, value = its occurrence frequency in selected BGCs.
    # # --------------Define dictionaries for statistics of BGCs (selected + discarded + all) and their products (only of selected BGCs) found in all antiSMASH-output------------------

    if side_options.verbose == True: print("\n\n")

    # # --------------Loop through list of input file(s) and analyze each BGC---------------
    for path_of_inputfile in inputpaths:
        # # -----------Get name and path of input file-----------------------
        name_of_inputfile = path_of_inputfile.split("/")[-1] # Note: this name might contain the suffix "renamed", added by the preprocessing step previously, to make name unique among all input file(s) of this task.
        path_of_inputfile = re.sub("_+renamed$", "", path_of_inputfile) # Get the original, correct path of input file in case this path was modified in previous preprocessing step. Note: only omit the string "renamed" at the end of the path (i.e. in name of file), not also somewhere in the middle of the path, if there is any.
        # # -----------Get name and path of input file-----------------------

        with open(path_of_inputfile, "r") as file_object:
            file_content = file_object.read()

        if len(re.findall(delimiter_btw_data_of_genes_and_DNA_seq_of_whole_BGC, file_content)) == 1 and label_for_file_of_one_BGC in file_content: # Important: check if input file (.gbk) contains only one BGC. Note: these textual tags are imported from module "analyze_and_assess.py" (see above).

            # # --------------Analysis of BGC------------------
            info_of_BGC, selection_status_for_BGC = analyze_and_assess.analyze_and_assess_BGC(file_content, param_for_preliminary_selection, param_for_main_selection, param_for_2nd_chance_selection) # Analyze the BGC in query file (according to input parameters) and return selection result.
            # # --------------Analysis of BGC------------------

            if side_options.verbose == True: print("> Complete analysis of BGC in file \"" + name_of_inputfile + "\"!")

            # # --------------Copy file of BGC if selected and update statistics------------------
            make_outputfiles_and_stats.copy_file_of_selected_BGC_and_update_stats( info_of_BGC, \
                                                                                   selection_status_for_BGC, \
                                                                                   name_of_inputfile ,\
                                                                                   path_of_inputfile, \
                                                                                   BGC_stats, \
                                                                                   product_stats ) # Note: "info_of_BGC" contains product of BGC that is needed to update statistics of selected BGCs and their products, if BGC is selected.
            # # --------------Copy file of BGC if selected and update statistics------------------

    end_analysis  = time.time() # Stop analysis time
    analysis_time = end_analysis - start_analysis # For results report.
    # # --------------Loop through list of input file(s) and analyze each BGC---------------

    # # --------------Report results of analysis and selection for all analyzed BGCs------------------

    print("\n\n\n>>> Task 2: Finished BGC-selection in directory \"" + names_and_paths.name_of_output_directory_from_antismash + "\" (analysis time = " + str(round(analysis_time, 1)) + " s) with the following values for the parameters:")

    # # --------------Print out selection parameters------------------
    print_to_terminal.print_parameters(param_for_preliminary_selection, param_for_main_selection, param_for_2nd_chance_selection)
    # # --------------Print out selection parameters------------------

    path_of_stats_dir = create.create_directory_if_not_exists(names_and_paths.path_of_directory_of_statistics) # Create path of directory for plots and statistics file, if this does not exist already. Directory is also created.

    if BGC_stats["All BGCs"] > 0: # Only make statistics if at least one BGC was found in directory for antiSMASH-output.
        # # --------------Make plots and show statistics------------------
        make_outputfiles_and_stats.plot_stats( param_for_preliminary_selection, \
                                               param_for_main_selection, \
                                               param_for_2nd_chance_selection, \
                                               BGC_stats, \
                                               product_stats, \
                                               path_of_stats_dir )

        print_to_terminal.print_BGC_stats(BGC_stats) # Print results of BGC-selection to Terminal.

        print_to_terminal.print_product_stats(product_stats) # Print product statistics to Terminal (this should be executed after printing statistics of BGC-selection).

        print("_"*200)
        # # --------------Make plots and show statistics------------------

    else: # In case no BGC was found in all analyzed antiSMASH-output directories:
        print("\n\n\n> No BGC was found!\n\n")
        print("_"*200)

    # # --------------Make statistics file------------------
    make_outputfiles_and_stats.make_stats_file( param_for_preliminary_selection, \
                                                param_for_main_selection, \
                                                param_for_2nd_chance_selection, \
                                                BGC_stats, \
                                                product_stats, \
                                                path_of_stats_dir ) # Make statistics file for all analyzed antiSMASH-output (note: this file is made even if there was no BGC found in all antiSMASH-output).
    # # --------------Make statistics file------------------

    # # --------------Report results of analysis and selection for all analyzed BGCs------------------

# # --------------------------------------------------------------------------TASK 2 OF PIPELINE: BGC-selection from antiSMASH-output--------------------------------------------------------------------------


# # --------------------------------------------------------------------------TASK 3 OF PIPELINE: Similarity analysis with BiGSCAPE--------------------------------------------------------------------------

def TASK_3(cutoffs):
    """
    Execute task 3 (similarity analysis by BiGSCAPE).

    Parameters
    ----------
    cutoffs : one or many float values in range [0, 1], separated by whitespace
        Maximum distance of BGCs in a GCF.

    Input files
    -----------
    Genbank (.gbk) file(s), each contains only one BGC (output from task 2 or can be provided externally).

    Returns
    -------
    None.

    Output files
    ------------
    An output directory that contains the file "index.html" with the results of similarity analysis.
    """
    print("\n\n\n>>> Initiating task 3 (similarity analysis by BiG-SCAPE CORASON)...")

    # # --------------Define paths and create directory for input and output of task---------------
    path_of_input_dir_for_task_3  = create.create_directory_if_not_exists(names_and_paths.path_of_directory_of_selected_BGCs)
    path_of_output_dir_for_task_3 = create.create_directory_if_not_exists(names_and_paths.path_of_directory_of_output_from_bigscape)

    create.create_directory_if_not_exists(names_and_paths.path_of_directory_of_thirdparty_programs) # Not so necessary: create directory for containing BiGSCAPE, if not existed.
    # # --------------Define paths and create directory for input and output of task---------------

    # # --------------Optional: clear BiGSCAPE-output directory before running BiGSCAPE------------------
    if side_options.clear_output_of_task_3 == True:
        shutil.rmtree(path_of_output_dir_for_task_3) # Remove whole directory containing BiGSCAPE results.
        create.create_directory_if_not_exists(path_of_output_dir_for_task_3) # Create directory for BiGSCAPE output again.
    # # --------------Optional: clear BiGSCAPE-output directory before running BiGSCAPE------------------

    # # --------------Checkpoint: check if directory of selected BGCs is not empty (input for this task)------------------
    if len(os.listdir(path_of_input_dir_for_task_3)) == 0:
        print("\n\n\n>>> Input directory \"" + names_and_paths.name_of_directory_of_selected_BGCs + "\" is empty! Task terminated!\n\n")
        print("_"*200)
        return # In case directory for selected BGCs is empty: end execution of task.
    # # --------------Checkpoint: check if directory of selected BGCs is not empty (input for this task)------------------

    # From here, directory that contains selected BGCs is not empty (i.e. input for this task is available) and proceed to the next codes:

    # # --------------Unzip all file(s)/folder(s) in input directory---------------
    unzip.unzip_all_files_and_folders_in_dir(path_of_input_dir_for_task_3)
    # # --------------Unzip all file(s)/folder(s) in input directory---------------

    # # --------------Loop through input directory and find path(s) of all input file(s) for task---------------
    inputpaths = [] # Define a list that will contain paths of all files of selected BGCs.

    for dir, subdirs, files in os.walk(path_of_input_dir_for_task_3, topdown=True): # "os.walk()": loop through all folders and files in directory with given path "path_of_input_dir_for_task_3". "dir": path of a certain directory found inside the directory of given path "path_of_input_dir_for_task_3", "subdirs": contains name(s) of subdirectory(-ies) in the directory "dir", "files": contains name(s) of file(s) in the directory "dir". "topdown": search from given directory with given path to its deepest file(s)/folder(s).
        for name_of_file in files: # Loop through all file(s) that can be found in directory of given path "path_of_input_dir_for_task_3", here directory of selected BGCs.
            if not name_of_file.startswith(tuple(names_and_paths.prefixes_of_names_of_incompatible_files)) and name_of_file.endswith(tuple(names_and_paths.file_extensions_of_antismash_outputfiles)): # Checkpoint: check if file is a correct input file for task (e.g. a .gbk file of a selected BGC).
                path_of_inputfile = os.path.join(dir, name_of_file)
                with open(path_of_inputfile, "r") as file_object:
                    file_content = file_object.read()

                if len(re.findall(delimiter_btw_data_of_genes_and_DNA_seq_of_whole_BGC, file_content)) == 1 and label_for_file_of_one_BGC in file_content: # Important: check if input file (.gbk) contains only one BGC.
                    inputpaths.append(path_of_inputfile)
    # # --------------Loop through input directory and find path(s) of all input file(s) for task---------------

    # # --------------Deduplicate input---------------
    deduplicate.remove_or_rename_files_with_duplicate_name(inputpaths) # Remove or rename paths in the list of antiSMASH-output files with duplicate name, which will make a list of paths of input files each with a unique name.
    # # --------------Deduplicate input---------------

    task_executed_successfully = False # Define a control variable for reporting results. This variable assumes at the beginning that the task is not (yet) successfully executed.

    task_executed_successfully = run_bigscape.run_bigscape(inputpaths, cutoffs)

    if task_executed_successfully == True:
        if side_options.analyze_query_BGCs_with_BGCs_from_MIBiG == True:
            added_text = " and BGCs from MIBiG database " # Add text to results report.
        else:
            added_text = " "
        print("\n\n\n>>> Task 3: Finished similarity analysis by BiG-SCAPE CORASON for query BGCs in directory \"" + names_and_paths.name_of_directory_of_selected_BGCs + "\"" + added_text + "with value for parameter \"cutoffs\" = " + str(cutoffs) + "!\n\n")
    print("_"*200)
    # Note: for task 3 (similarity analysis by BiGSCAPE), no need to report run time as BiGSCAPE already reports this ("Main function took ... s").

# # --------------------------------------------------------------------------TASK 3 OF PIPELINE: Similarity analysis with BiGSCAPE--------------------------------------------------------------------------


# # --------------------------------------------------------------------------USER-INTERFACE (starting point of main program)--------------------------------------------------------------------------

def Entry_Point():
    """
    Start user-interface where user can specify task(s) to be executed.

    Parameters
    ----------
    None.

    Input from user:
    ----------------
    One or many numbers, e.g. 1, 2, 3, 12, 23, 13, 123 or 4.

    Returns
    -------
    None.
    """
    os.system("clear") # Should this be left out?
    print("-"*70 + "+"*30 + "-"*70)
    print(" "*15 + "WELCOME TO THE BIOINFORMATIC MULTIPROGRAM PIPELINE FOR AUTOMATED IDENTIFICATION, SELECTION AND CLUSTERING OF BIOSYNTHETIC GENE CLUSTERS!")
    print("-"*70 + "+"*30 + "-"*70)

    if side_options.prompt_user_to_input_tasks_to_execute == True: # In case user is prompted to specify functions to execute (default):
        print("\n\n\n>>> THIS PIPELINE CAN PERFORM THE FOLLOWING TASKS:\n")

        list_of_executable_tasks = {
        "1" : "Detection of biosynthetic gene clusters by the program antiSMASH",
        "2" : "Selection of most likely intact and functional biosynthetic gene clusters",
        "3" : "Clustering of similar biosynthetic gene clusters by the program BiG-SCAPE CORASON",
        "4" : "All executable tasks"
        }

        print(tabulate(list_of_executable_tasks.items(), tablefmt="fancy_grid")) # Present all executable tasks by pipeline.

        list_of_tasks_to_execute = list(input("\n>>> Please specify the task(s) to be performed (e.g. 1, 2, 12, etc.): ")) # Split input into list of symbols to check if "1", "2", "3", or "4" is included (see below).

        while True:
            if ("1" not in list_of_tasks_to_execute) and ("2" not in list_of_tasks_to_execute) and ("3" not in list_of_tasks_to_execute) and ("4" not in list_of_tasks_to_execute): # In case the given numbers for executable tasks are not included in input (i.e. invalid input):
                print(">>> Invalid input! Please try again!")
                list_of_tasks_to_execute = list(input("\n>>> Please specify the task(s) to be performed (e.g. 1, 2, 12, etc.): "))
                continue
            else:
                break

        print("\n\n" + "_"*200)

        # # --------------Get input of value(s) for parameter(s) needed for all task(s)------------------
        # Note: user should be prompted at the beginning (i.e. before starting to execute all task(s)) to input value(s) for all parameter(s) needed in all specified task(s).
        if side_options.prompt_user_to_input_values_for_parameters == True:    # Ask user to input value(s) for parameter(s).

            # # --------------For task 2 of pipeline: acquire values of parameters for selection------------------
            if ("2" in list_of_tasks_to_execute) or ("4" in list_of_tasks_to_execute):
                param_for_preliminary_selection, param_for_main_selection, param_for_2nd_chance_selection = input_parameters.for_task_2()
            # # --------------For task 2 of pipeline: acquire values of parameters for selection------------------

            # # --------------For task 3 of pipeline: acquire value of parameter "cutoffs"------------------
            if ("3" in list_of_tasks_to_execute) or ("4" in list_of_tasks_to_execute):
                cutoffs = input_parameters.for_task_3()
                # Note: option to use BGCs from MIBiG database is not asked here as an input parameter, as this option is most often used. This option can however be changed in module "side_options.py".
            # # --------------For task 3 of pipeline: acquire value of parameter "cutoffs"------------------

        else:                                                                  # Otherwise, use predefined value(s) for parameter(s) in module "input_parameters.py".
            # # --------------For task 2 of pipeline: acquire values of parameters for selection------------------
            if ("2" in list_of_tasks_to_execute) or ("4" in list_of_tasks_to_execute):
                param_for_preliminary_selection,  param_for_main_selection,  param_for_2nd_chance_selection   =   input_parameters.param_for_preliminary_selection,  input_parameters.param_for_main_selection,  input_parameters.param_for_2nd_chance_selection
            # # --------------For task 2 of pipeline: acquire values of parameters for selection------------------

            # # --------------For task 3 of pipeline: acquire value of parameter "cutoffs"------------------
            if ("3" in list_of_tasks_to_execute) or ("4" in list_of_tasks_to_execute):
                cutoffs = input_parameters.cutoffs
            # # --------------For task 3 of pipeline: acquire value of parameter "cutoffs"------------------
        # # --------------Get input of value(s) for parameter(s) needed for all task(s)------------------

        # # --------------Execute all specified task(s)------------------
        if ("1" in list_of_tasks_to_execute) or ("4" in list_of_tasks_to_execute):
            TASK_1() # Execute task 1 (i.e. gene finding by antiSMASH) if specified.

        if ("2" in list_of_tasks_to_execute) or ("4" in list_of_tasks_to_execute):
            TASK_2(param_for_preliminary_selection, param_for_main_selection, param_for_2nd_chance_selection) # Execute task 2 (i.e. BGC-selection) with input values for parameters, if specified.

        if ("3" in list_of_tasks_to_execute) or ("4" in list_of_tasks_to_execute):
            TASK_3(cutoffs) # Execute task 3 (i.e. similarity analysis by BiGSCAPE) if specified.

        # Note: do not use "if...elif..." block here as that would only allow one task at maximum to be executed!
        # # --------------Execute all specified task(s)------------------
        
        # # --------------Change permission of all files and folders in common directory------------------
        change_permit.change_permit_of_all_folders_and_files_in_common_dir() # Allow access to all output files (in case some output files are created by docker, e.g. after running antiSMASH and BiGSCAPE, and initially not accessible by user).
        # # --------------Change permission of all files and folders in common directory------------------

        print("\n\n\n>>> All specified task(s) completed!\n\n") # Exit point: main program will end here if executed successfully.

    else: # In case "prompt_user_to_input_tasks_to_execute" is set to False (i.e. assume user would like to execute all tasks without being asked):
        # # --------------Get input of values for parameters needed for all tasks------------------
        # Note: user should be prompted at the beginning (i.e. before starting to execute all tasks to input values for all parameters needed in all tasks.
        if side_options.prompt_user_to_input_values_for_parameters == True:    # Ask user to input values for parameters for all tasks.

            # # --------------For task 2 of pipeline: acquire values of parameters for selection------------------
            param_for_preliminary_selection, param_for_main_selection, param_for_2nd_chance_selection = input_parameters.for_task_2()
            # # --------------For task 2 of pipeline: acquire values of parameters for selection------------------

            # # --------------For task 3 of pipeline: acquire value of parameter "cutoffs"------------------
            cutoffs = input_parameters.for_task_3()
                # Note: option to use BGCs from MIBiG database is not asked here as an input parameter, as this option is most often used. This option can however be changed in module "side_options.py".
            # # --------------For task 3 of pipeline: acquire value of parameter "cutoffs"------------------

        else:                                                                  # Otherwise, use predefined values for parameters in module "input_parameters.py".
            # # --------------For task 2 of pipeline: acquire values of parameters for selection------------------
            param_for_preliminary_selection,  param_for_main_selection,  param_for_2nd_chance_selection   =   input_parameters.param_for_preliminary_selection,  input_parameters.param_for_main_selection,  input_parameters.param_for_2nd_chance_selection
            # # --------------For task 2 of pipeline: acquire values of parameters for selection------------------

            # # --------------For task 3 of pipeline: acquire value of parameter "cutoffs"------------------
            cutoffs = input_parameters.cutoffs
            # # --------------For task 3 of pipeline: acquire value of parameter "cutoffs"------------------
        # # --------------Get input of values for parameters needed for all tasks------------------

        # # --------------Execute all tasks------------------
        TASK_1()

        TASK_2(param_for_preliminary_selection, param_for_main_selection, param_for_2nd_chance_selection)

        TASK_3(cutoffs)
        # # --------------Execute all tasks------------------
        
        # # --------------Change permission of all files and folders in common directory------------------
        change_permit.change_permit_of_all_folders_and_files_in_common_dir() # Allow access to all output files (in case some output files are created by docker, e.g. after running antiSMASH and BiGSCAPE, and initially not accessible by user).
        # # --------------Change permission of all files and folders in common directory------------------

        print("\n\n\n>>> All executable tasks completed!\n\n") # Exit point: main program will end here if executed successfully.

# # --------------------------------------------------------------------------USER-INTERFACE (starting point of main program)--------------------------------------------------------------------------


if __name__ == '__main__':
    Entry_Point() # Call main function that starts pipeline, only if this script is executed directly (and not as an imported module).


# Note to myself: sys.argv[1] can be used to take path of input directory from argument of running command. However, the question is, whether the user is willing to type a lot...
