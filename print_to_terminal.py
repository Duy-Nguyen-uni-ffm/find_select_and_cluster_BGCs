''' This module prints input parameters and statistics of BGC-selection and product(s) (of selected BGCs) to the Text Command Terminal. '''


import pandas as pd
from   tabulate import tabulate

import side_options
import stats_utils


# # -----------Show input parameters-----------------------
# Note: this function is used in main program "start_and_command.py".
def print_parameters(param_for_preliminary_selection, param_for_main_selection, param_for_2nd_chance_selection):
    """
    Print used values for parameters to Command Terminal.

    Parameters
    ----------
    param_for_preliminary_selection : dict of {str : str}
        Parameter for preliminary selection, i.e. minimum number of core genes.
    param_for_main_selection        : dict of {str : str}
        Parameters for main selection, i.e. minimum length of cluster (in bp), minimum distance of each core gene to edges of cluster (in bp) and minimum number of additional biosynthetic genes.
    param_for_2nd_chance_selection  : dict of {str : str}
        Parameter for second-chance selection, i.e. minimum number of additional biosynthetic genes.

    Returns
    -------
    None.
    """
    print("\n\n>> For preliminary selection:", pd.DataFrame(param_for_preliminary_selection, index = [""]).T) # index = [""]): no index, .T: transpose

    print("\n>> For main selection:", pd.DataFrame(param_for_main_selection, index = [""]).T) # index = [""]): no index, .T: transpose

    print("\n>> For second-chance selection:", pd.DataFrame(param_for_2nd_chance_selection, index = [""]).T) # index = [""]): no index, .T: transpose
# # -----------Show input parameters-----------------------


# # -----------Print statistics of BGC-selection----------------------
def print_BGC_stats(BGC_stats):
    """
    Print overall statistics of BGC-selection to Command Terminal.

    Parameters
    ----------
    BGC_stats : dict of {str : int}
        Overall statistics of BGC-selection.

    Returns
    -------
    None.
    """
    # Note: "BGC_stats["All BGCs"]" must > 0 for this function. This is already checked in main program "start_and_command.py"
    print("\n\n\n>>> Results of BGC-selection:\n")
    DataFrame_of_BGC_stats = pd.DataFrame(BGC_stats, index=[""]) # Make DataFrame of BGC statistics. This is needed for adding the new row "Percentages" (see below).
    DataFrame_of_BGC_stats.loc["Percentages"] = [ "{:.2%}".format( DataFrame_of_BGC_stats.iloc[0,i] / DataFrame_of_BGC_stats.iloc[0,2] ) for i in range(len(BGC_stats)) ] # Before print out: add a row for percentages to DataFrame ("DataFrame_of_BGC_stats.iloc[0,2]" = Number of all analyzed BGCs)
    print(tabulate(DataFrame_of_BGC_stats, headers='keys', showindex=False, tablefmt="fancy_grid"))
# # -----------Print statistics of BGC-selection----------------------


# # -----------Print statistics of product(s) of selected BGCs----------------------
def print_product_stats(product_stats):
    """
    Print overall statistics of product(s) of selected BGCs to Command Terminal.

    Parameters
    ----------
    product_stats : dict of {str : int}
        Overall statistics of product(s) of selected BGCs.

    Returns
    -------
    None.
    """
    # # --------------Group or sort all product(s) before printing to Terminal------------------
    if product_stats != {}: # Only sort if at least one product of selected BGCs is present.
        if side_options.group_products_in_predefined_groups == True:
            product_stats = stats_utils.group_products(product_stats) # Optional: group all products (of selected BGCs) in predefined groups.
        else:
            product_stats = dict(sorted(product_stats.items(), key=lambda x: x[1], reverse=False)) # Sort products according to their frequencies. Note: "product_stats" is a dict Object, not a list; .items() returns a list of tuples of key:value which "sorted()" can be applied on; x[1] means sorting according to values, i.e. frequency of products.
    # # --------------Group or sort all product(s) before printing to Terminal------------------

    print("\n\n\n>>> Product(s) of selected BGCs:\n")
    if product_stats != {}:
        DataFrame_of_product_stats = pd.DataFrame(product_stats, index=[""])
        print(tabulate(DataFrame_of_product_stats, headers='keys', showindex=False, tablefmt="fancy_grid"), "\n\n")
    else:
        print("> No BGC was selected and therefore no product of selected BGCs!\n\n") # Note: if there is no product of selected BGCs, then there was no BGC selected.
# # -----------Print statistics of product(s) of selected BGCs----------------------
