''' This module keeps the Boolean values for the "quick-switch" variables (i.e. control variables) that activate or deactivate certain optional functions/features that are coded in other modules. '''


# IMPORTANT: Only assign "True" or "False" for the following option-variables!
# # -----------Options for dealing with name collision of input or output-----------------------
analyze_files_with_same_name_but_different_content          = True              # True (recommended): rename and analyze in all executable tasks input files with duplicate name but different file content. This applies to all executable tasks.
                                                                                # False: skip analyzing input files with duplicate name, even if they have different content. This applies to all executable tasks.

rename_output_if_name_collides                              = True              # True (recommended): before analyzing input files, change name of their output files/folders in case their name would collide with other already existing output. This applies to all executable tasks.
                                                                                # False: skip analyzing input files if their output files/folders would have same name with other already existing output. This applies to all executable tasks.
# # -----------Options for dealing with name collision of input or output-----------------------


# # -----------Side option-----------------------
verbose                                                     = True              # True: print to text terminal verbose information, e.g. for debugging (encoded by the commands "print()" in main program "start_and_command.py").
                                                                                # False: print only important results and information to text terminal (note: this option has no influence on standard output of antiSMASH and BiGSCAPE).
# # -----------Side option-----------------------


# # -----------Options of user-interface-----------------------
prompt_user_to_input_tasks_to_execute                       = True              # True (recommended): by every run of the pipeline, the user will be prompted to specify task(s) to be executed by pipeline.
                                                                                # False: by every run of the pipeline, the pipeline will perform all executable tasks.

prompt_user_to_input_values_for_parameters                  = True              # True: the user will be prompted to input values of parameters needed for all task(s) in each run of the pipeline.
                                                                                # False: the pipeline will use the predefined values of parameters given in module "input_parameters.py".
# # -----------Options of user-interface-----------------------


# # -----------Option in task 1 (gene prediction)-----------------------
clear_output_of_task_1                                      = False             # True: empty output directory of task before performing task. Use this option when wish to execute this one task only, otherwise next task will not have input. This option can avoid name collision of output as well as interference of results and reduce size of output directory.
                                                                                # Note: be careful not to remove important files or data unintentionally!
# # -----------Option in task 1 (gene prediction)-----------------------


# # -----------Options in task 2 (BGC-selection)-----------------------
clear_output_of_task_2                                      = True             # True: empty output directory of task before performing task. Use this option when wish to execute this one task only, otherwise next task will not have input. This option can avoid name collision of output as well as interference of results and reduce size of output directory.
                                                                                # Note: be careful not to remove important files or data unintentionally!

group_products_in_predefined_groups                         = False             # True: group all found products into predefined groups to simplify output products (these product groups can be adapted in module "stats_utils.py").
                                                                                # False: all found products will only be sorted according to their frequencies.

show_plots                                                  = False             # True: interrupt and show plots during the execution of pipeline. The pipeline will resume executing specified task(s), once the window showing the plot has been closed.

add_note_to_plot                                            = False             # True: add an annotation note to plots of BGC-selection and product(s) of selected BGCs (note contains e.g. values of input parameters).

fill_background_plot_with_grey                              = False             # True: fill background of all plots (with grey) for better contrast.
# # -----------Options in task 2 (BGC-selection)-----------------------


# # -----------Options in task 3 (similarity analysis)-----------------------
clear_output_of_task_3                                      = False             # True: empty output directory of task before performing task. Use this option when wish to execute this one task only, otherwise next task will not have input. This option can avoid name collision of output as well as interference of results and reduce size of output directory.
                                                                                # Note: be careful not to remove important files or data unintentionally!

analyze_query_BGCs_with_BGCs_from_MIBiG                     = True              # True (recommended): analyze query BGCs with BGCs from database MIBiG.
# # -----------Options in task 3 (similarity analysis)-----------------------
