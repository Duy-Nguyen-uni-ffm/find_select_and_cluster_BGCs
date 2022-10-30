''' This module stores predefined values for the parameters needed by all tasks, which will be used directly if the option "prompt_user_to_input_values_for_parameters" in module "side_options.py"
    is set to False. Otherwise this module contains functions that ask user for input values of the parameters for the corresponding tasks. '''


# # ----------------------------------------------------------------------------------------------------------------ALTERNATIVE 1: Use predefined values for all parameters----------------------------------------------------------------------------------------------------------------
# Note: the predefined values below can all be adapted freely, they can however only all be used if the option "prompt_user_to_input_values_for_parameters" in "side_options.py" is set to False (in that case, the main program "start_and_command.py" will not execute all the functions below).

# # --------------For task 2 of pipeline: predefined parameters that will be used in three selection rounds------------------
# For preliminary selection:
min_num_of_core_genes                                       = 2

# For main selection:
min_length                                                  = 20000     # Minimum sequence length of BGC (in bp)
min_distance                                                = 5000      # Minimum distance of each core gene to both edges of BGC (in bp)
min_num_of_additional_genes_for_main_selection              = 3         # Minimum number of additional biosynthetic genes in BGC (number used for main selection)

# For second-chance selection (examination of BGCs that only passed preliminary selection but failed main selection):
min_num_of_additional_genes_for_2nd_chance_selection        = 5         # Should be bigger than corresponding parameter in the main selection, since second-chance selection should be stricter

# Store predefined parameters:
param_for_preliminary_selection = {}
param_for_main_selection        = {}
param_for_2nd_chance_selection  = {}

param_for_preliminary_selection["Minimum number of core genes"]                                     = str(min_num_of_core_genes)

param_for_main_selection["Minimum length (in bp)"]                                                  = str(min_length)
param_for_main_selection["Minimum distance (in bp)"]                                                = str(min_distance)
param_for_main_selection["Minimum number of additional biosynthetic genes"]                         = str(min_num_of_additional_genes_for_main_selection)

param_for_2nd_chance_selection["Minimum number of additional biosynthetic genes"]                   = str(min_num_of_additional_genes_for_2nd_chance_selection)
# # --------------For task 2 of pipeline: predefined parameters that will be used in three selection rounds------------------


# # --------------For task 3 of pipeline: predefined parameter for similarity analysis by BiGSCAPE------------------
cutoffs                                                                                             = "0.7" # One or many values that will be used to group BGCs into families (in case more than one value is passed, e.g. "0.8 0.9", bigscape will establish an analysis for each value). Important: this variable can only take float value(s) in range (0.0, 1.0].
# # --------------For task 3 of pipeline: predefined parameter for similarity analysis by BiGSCAPE------------------
# # ----------------------------------------------------------------------------------------------------------------ALTERNATIVE 1: Use predefined values for all parameters----------------------------------------------------------------------------------------------------------------


# # ----------------------------------------------------------------------------------------------------------------ALTERNATIVE 2: Prompt user to input values for all parameters----------------------------------------------------------------------------------------------------------------
# Note: if the functions below are executed (i.e. if "prompt_user_to_input_values_for_parameters" in "side_options.py" is set to True), the above predefined values for parameters will not be used.

# # --------------For task 2 of pipeline: prompt user to input parameters for the three selection rounds------------------

def for_task_2():
    """
    Prompt user to input values for parameters that will be used in task 2 (BGC-selection).

    Parameters
    ----------
    None.

    Input from user:
    ----------------
    Positive integer values for parameters.

    Returns
    -------
    param_for_preliminary_selection     : dict of {str : str}
        Parameter for preliminary selection, i.e. minimum number of core genes.
    param_for_main_selection            : dict of {str : str}
        Parameters for main selection, i.e. minimum length of cluster (in bp), minimum distance of each core gene to edges of cluster (in bp) and minimum number of additional biosynthetic genes.
    param_for_2nd_chance_selection      : dict of {str : str}
        Parameter for second-chance selection, i.e. minimum number of additional biosynthetic genes.
    """
    # # --------------Check if input value for parameter is an integer------------------
    def check_value_of_input(parameter, name_of_parameter):
        """
        Check if input values for parameters are valid, i.e. positive integer numbers.

        Parameters
        ----------
        parameter           : str
            Last input value for parameter.
        name_of_parameter   : str
            Name of parameter (for printing input command again in case last input is invalid).

        Input from user:
        ----------------
        In case last input for parameter is invalid, a positive integer value for the parameter.

        Returns
        -------
        parameter : str
            A positive integer value for the parameter.
        """
        while not parameter.isnumeric():
            print("> Input should be a non negative integer value! Please try again!")     # In case input value for parameter is not an integer (i.e. invalid input).
            if   name_of_parameter.startswith(("minimum length", "minimum distance")):     # "name_of_parameter" would either be "minimum length of cluster"                            or "minimum distance of each core gene to both edges of cluster" (both have unit bp).
                parameter = input("> Input " + name_of_parameter + " (in bp) = ")
            elif name_of_parameter.startswith("minimum number"):                           # "name_of_parameter" would either be "minimum number of core biosynthetic genes in cluster" or "minimum number of additional biosynthetic genes in cluster" (both are unit-less).
                parameter = input("> Input " + name_of_parameter + " (non negative integer) = ")

        return parameter # Note: "parameter" has type string
    # # --------------Check if input value for parameter is an integer------------------

    # # --------------Prompt user to input values for selection parameters and check if input values are valid------------------
    print("\n\n\n>>> For task 2 (BGC-selection), please input values for the following parameters:\n")
    print("\n>> For preliminary selection:")
    min_num_of_core_genes = input("> Input minimum number of core biosynthetic genes in cluster (non negative integer) = ")
    min_num_of_core_genes = check_value_of_input(parameter = min_num_of_core_genes, name_of_parameter = "minimum number of core biosynthetic genes in cluster")


    print("\n>> For main selection:")
    min_length = input("> Input minimum length of cluster (in bp, e.g. 10000) = ")
    min_length = check_value_of_input(parameter = min_length, name_of_parameter = "minimum length of cluster")

    min_distance = input("> Input minimum distance of each core gene to both edges of cluster (in bp, e.g. 3000) = ")
    min_distance = check_value_of_input(parameter = min_distance, name_of_parameter = "minimum distance of each core gene to both edges of cluster")
    while not int(min_distance)*2 <= int(min_length):
        print("> Invalid input! Minimum distance should be twice smaller than minimum length of cluster! Please input a different value!")
        min_distance = input("> Input minimum distance of each core gene to both edges of cluster (in bp, e.g. 3000) = ")
        min_distance = check_value_of_input(parameter = min_distance, name_of_parameter = "minimum distance of each core gene to both edges of cluster")

    min_num_of_additional_genes_for_main_selection = input("> Input minimum number of additional biosynthetic genes in cluster (non negative integer) = ")
    min_num_of_additional_genes_for_main_selection = check_value_of_input(parameter = min_num_of_additional_genes_for_main_selection, name_of_parameter = "minimum number of additional biosynthetic genes in cluster")


    print("\n>> For second-chance selection:")
    min_num_of_additional_genes_for_2nd_chance_selection = input("> Input minimum number of additional biosynthetic genes in cluster (non negative integer) = ")
    min_num_of_additional_genes_for_2nd_chance_selection = check_value_of_input(parameter = min_num_of_additional_genes_for_2nd_chance_selection, name_of_parameter = "minimum number of additional biosynthetic genes in cluster")
    print("\n\n" + "_"*200)
    # # --------------Prompt user to input values for selection parameters and check if input values are valid------------------

    # # --------------Store input values for parameters----------------
    param_for_preliminary_selection = {}
    param_for_main_selection        = {}
    param_for_2nd_chance_selection  = {}

    param_for_preliminary_selection["Minimum number of core genes"]                     = min_num_of_core_genes

    param_for_main_selection["Minimum length (in bp)"]                                  = min_length
    param_for_main_selection["Minimum distance (in bp)"]                                = min_distance
    param_for_main_selection["Minimum number of additional biosynthetic genes"]         = min_num_of_additional_genes_for_main_selection

    param_for_2nd_chance_selection["Minimum number of additional biosynthetic genes"]   = min_num_of_additional_genes_for_2nd_chance_selection
    # # --------------Store input values for parameters----------------

    return param_for_preliminary_selection, param_for_main_selection, param_for_2nd_chance_selection

# # --------------For task 2 of pipeline: prompt user to input parameters for the three selection rounds------------------


# # --------------For task 3 of pipeline: prompt user to input parameter for the similarity analysis by BiGSCAPE------------------

def for_task_3():
    """
    Prompt user to input value for parameter that will be used in task 3 (similarity analysis by BiGSCAPE).

    Parameters
    ----------
    None.

    Input from user:
    ----------------
    One or many positive float values, separated by whitespace, for parameter.

    Returns
    -------
    cutoffs : str
        Positive float value(s) for parameter "cutoffs".
    """
    # # --------------Check if input value for parameter is a float value between 0.0 and 1.0------------------
    def check_value_of_input(parameter, name_of_parameter):
        """
        Check if input value(s) for parameter is/are valid, i.e. positive float number(s) each between 0 and 1.

        Parameters
        ----------
        parameter           : str
            Last input value for parameter.
        name_of_parameter   : str
            Name of parameter (for printing input command again in case last input is invalid).

        Input from user:
        ----------------
        In case last input for parameter is invalid, one or many positive float values, separated by whitespace.

        Returns
        -------
        parameter : str
            One or many positive float values for the parameter.
        """
        valid_input = False # Assume input for parameter is invalid.
        while True:
            for value in parameter.split(): # Split input value(s) into whitespace-separated values, if multiple values are given, and check each value:
                try:
                    value = float(value) # Check if value can be converted into float type.
                except:
                    print("> Input should be real number(s) between 0.0 and 1.0! Please try again!") # In case one input value for parameter is not a real number at all (i.e. invalid input).
                    parameter = input("> Input " + name_of_parameter + " (i.e. cutoffs, e.g. 0.3) = ")
                    valid_input = False
                    break # Break loop to input again (with "valid_input" = False).
                if float(value) < 0.0 or float(value) > 1.0:
                    print("> Input should be real number(s) between 0.0 and 1.0! Please input different value(s)!") # In case one input value for parameter is a real number but not between 0.0 and 1.0 (i.e. invalid input).
                    parameter = input("> Input " + name_of_parameter + " (i.e. cutoffs, e.g. 0.3) = ")
                    valid_input = False
                    break # Break loop to input again (with "valid_input" = False).
                valid_input = True

            if valid_input == True:
                break # In case all input value(s) for parameter is/are real number(s) between 0.0 and 1.0, i.e. valid input, break loop for checking.
        return parameter # Note: "parameter" has type string.
    # # --------------Check if input value for parameter is a float value between 0.0 and 1.0------------------

    # # --------------Prompt user to input value for parameter and check if input value is valid------------------
    print("\n\n\n>>> For task 3 (similarity analysis by BiG-SCAPE CORASON), please input value for the following parameter:\n")
    print("\n>> For similarity analysis:")
    cutoffs = input("> Input maximum distance of clusters for similarity analysis (i.e. cutoffs, e.g. 0.3) = ").strip() # Take input value(s) for parameter "cutoffs" and remove leading/trailing spaces, if there are any.
    cutoffs = check_value_of_input(parameter = cutoffs, name_of_parameter = "maximum distance of clusters for similarity analysis")
    print("\n\n" + "_"*200)
    # Note: option to use BGCs from MIBiG database is not asked here as a parameter as this option is most often used. This option can however be changed in module "side_options.py".
    # # --------------Prompt user to input value for parameter and check if input value is valid------------------

    return cutoffs

# # --------------For task 3 of pipeline: prompt user to input parameter for the similarity analysis by BiGSCAPE------------------

# # ----------------------------------------------------------------------------------------------------------------ALTERNATIVE 2: Prompt user to input values for all parameters----------------------------------------------------------------------------------------------------------------
