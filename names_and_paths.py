''' This module contains names and absolute paths of important directories and files that are used by other modules. It also contains prefixes in names of files and folders that the pipeline can use to recognize as unreadable/unanalyzable files/folders (i.e. incompatible files/folders)
    and skip these, but also file extension(s) of input files that are compatible for antiSMASH and file extension(s) of output files from antiSMASH. '''


import os


# Names/prefixes of names/file extensions of relevant files and directories:
name_of_common_directory                                        = os.path.dirname(os.path.realpath(__file__)).split("/")[-1] # Common or parent directory that contains all scripts of pipeline as well as input, output directories.

name_of_input_directory_for_antismash                           = "input_for_antiSMASH"
name_of_output_directory_from_antismash                         = "output_from_antiSMASH"
name_of_directory_of_selected_BGCs                              = "selected_BGCs"
name_of_input_directory_for_bigscape                            = "input_for_BiGSCAPE"
name_of_output_directory_from_bigscape                          = "output_from_BiGSCAPE"

name_of_directory_of_statistics                                 = "statistics"
name_of_directory_of_info_files                                 = "info"
name_of_directory_of_thirdparty_programs                        = "thirdparty_programs" # This directory contains programs from third party such as antiSMASH, BiG-SCAPE.

name_of_statistics_file                                         = "statistics_file.txt"
name_of_plot_of_BGC_statistics                                  = "BGCs.png"
name_of_plot_of_product_statistics                              = "products.png"

prefixes_of_names_of_incompatible_files                         = [ "." ] # Prefix(es) of names of incompatible files not to analyze by antiSMASH, BiGSCAPE and in BGC-selection.
# file_extensions_of_files_not_to_analyze                         = [ ".zip", ".tar" ] # Types of files and folders not to analyze.
file_extensions_of_antismash_inputfiles                         = [ ".fasta" ] # File extension(s) of files that will be input to antiSMASH.
file_extensions_of_antismash_outputfiles                        = [ ".gbk" ] # File extension(s) of output files from antiSMASH that will be recognized and analyzed in BGC-selection and by BiGSCAPE.
# Note to myself: should use lists, not tuples, to store these prefixes/file extensions, otherwise 1-element tuples will be unpacked in single elements.


# Paths of important directories:
common_path                                                     = os.path.dirname(os.path.realpath(__file__)) + "/" # Path of main or common directory, which contains all files and directories created or used by this pipeline.

path_of_directory_of_input_for_antismash                        = common_path + name_of_input_directory_for_antismash + "/"
path_of_directory_of_output_from_antismash                      = common_path + name_of_output_directory_from_antismash + "/"
path_of_directory_of_selected_BGCs                              = common_path + name_of_directory_of_selected_BGCs + "/"
path_of_directory_of_input_for_bigscape                         = common_path + name_of_input_directory_for_bigscape + "/"
path_of_directory_of_output_from_bigscape                       = common_path + name_of_output_directory_from_bigscape + "/"

path_of_directory_of_statistics                                 = common_path + name_of_directory_of_statistics + "/"
path_of_directory_of_thirdparty_programs                        = common_path + name_of_directory_of_thirdparty_programs + "/"
# Note: os.path.join() could be used here, but be careful with the slash "/" in paths.
