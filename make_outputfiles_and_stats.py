''' This module operates the following functions: (1) copy Genbank antiSMASH-output files of selected BGCs to directory for selected BGCs, (2) calculate statistics of BGCs and product(s) of selected BGCs, (3) plot all statistics and (4) create files (.txt) that contain calculated statistics. '''


import os
import re
import shutil
import pandas as pd
import matplotlib.pyplot as plt
from   datetime import datetime

import names_and_paths
import side_options
import stats_utils


# # -----------Copy Genbank file of selected BGC to directory of selected BGCs and update statistics-----------------------
def copy_file_of_selected_BGC_and_update_stats( info_of_BGC, selection_status_for_BGC, \
                                                name_of_inputfile, path_of_file_for_BGC, \
                                                BGC_stats, product_stats ):
    """
    Copy Genbank (.gbk) file of BGC, if selected by main or second-chance selection, from the input directory for task 2 to its output directory, i.e. directory of all selected BGCs, and update statistics.

    Parameters
    ----------
    info_of_BGC                 : dict of {str : str}
        General information of BGC: name of BGC, length of BGC (in bp) and product(s) of BGC.
    selection_status_for_BGC    : str
        Selection result of BGC: either "discarded", "passed main selection" or "passed second-chance selection".
    name_of_inputfile           : str
        Name of Genbank (.gbk) file containing BGC.
    path_of_file_for_BGC        : str
        Path of Genbank (.gbk) file containing BGC.
    BGC_stats                   : dict of {str : int}
        Statistics of BGC-selection.
    product_stats               : dict of {str : int}
        Statistics of product(s) of selected BGCs.

    Returns
    -------
    None.

    Output files
    ------------
    A copy of Genbank (.gbk) file of BGC in output directory for task 2, if BGC is selected by main or second-chance selection. Else no output file.
    """
    # # -----------Add one count to corresponding entry in statistics dictionary-----------------------
    def update_stats(stats_dict, entry):
        """
        Update a statistics.

        Parameters
        ----------
        stats_dict  : dict of {str : int}
            A dictionary that stores statistics (e.g. for BGC-selection or product(s) of selected BGCs).
        entry       : str
            An entry of statistics (e.g. a product or "BGCs selected")

        Returns
        -------
        None (the given statistics will however be updated).
        """
        if entry not in stats_dict:
            stats_dict[entry]  = 1
        elif entry in stats_dict:
            stats_dict[entry] += 1
    # # -----------Add one count to corresponding entry in statistics dictionary-----------------------

    # # -----------Case 1: if BGC is selected by main or by second-chance selection-----------------------
    if selection_status_for_BGC == "passed main selection" or selection_status_for_BGC == "passed second-chance selection": # Only copy file for BGC if BGC is selected by main or by second-chance selection

        # # -----------Prepare destination path for copying file-----------------------
        file_extension                      = re.search( "|".join(tuple(names_and_paths.file_extensions_of_antismash_outputfiles)), name_of_inputfile ).group() # Get file extension from name of file (first match) (".group()" returns only the matching group, which is here the file extension).
        name_of_inputfile                   = re.sub(file_extension, "", name_of_inputfile) + file_extension # In case name has suffix "renamed", move file extension to the end of name.
        destination_path_for_copying_file   = names_and_paths.path_of_directory_of_selected_BGCs + name_of_inputfile
        # # -----------Prepare destination path for copying file-----------------------

        # # -----------Checkpoint: if copy path already exists-----------------------
        if os.path.isfile(destination_path_for_copying_file):
            if side_options.rename_output_if_name_collides == True:
                destination_path_for_copying_file += "__latest_output"
                while os.path.isfile(destination_path_for_copying_file):
                    destination_path_for_copying_file = destination_path_for_copying_file.replace("__latest_output$", "___latest_output") # Rename destination path for copying file until this path does not conflict with path(s) of other existing output file(s).
            else:
                return # Stop analyzing file.
        # # -----------Checkpoint: if copy path already exists-----------------------

        # # -----------Copy file of selected BGC to directory of all selected BGCs-----------------------
        shutil.copyfile(path_of_file_for_BGC, destination_path_for_copying_file) # Copy file for selected BGC to directory of selected BGCs ("selected_BGCs")
        # # -----------Copy file of selected BGC to directory of all selected BGCs-----------------------

        # # -----------Update statistics (BGCs + products)-----------------------
        update_stats(stats_dict = BGC_stats, entry = "BGCs selected")

        products_of_BGC = "+".join(info_of_BGC["Product(s) of BGC"]) # Note: "products_of_BGC" is always a nonempty list if "selection_status_for_BGC" is not "discarded". Furthermore, if the BGC has more than one product, the products will be sorted alphabetically.
        update_stats(stats_dict = product_stats, entry = products_of_BGC) # Note: if there is no BGC selected, there will be no product of selected BGCs in this statistics.
        # # -----------Update statistics (BGCs + products)-----------------------
    # # -----------Case 1: if BGC is selected by main or by second-chance selection-----------------------

    # # -----------Case 2: if BGC is not selected-----------------------
    elif selection_status_for_BGC == "discarded":
        update_stats(stats_dict = BGC_stats, entry = "BGCs discarded")
    # # -----------Case 2: if BGC is not selected-----------------------

    # # -----------For both cases: update number of all analyzed BGCs-----------------------
    update_stats(stats_dict = BGC_stats, entry = "All BGCs")
    # # -----------For both cases: update number of all analyzed BGCs-----------------------
# # -----------Copy Genbank file of selected BGC to directory of selected BGCs and update statistics-----------------------


# # -----------Make plots for statistics-----------------------
def plot_stats( param_for_preliminary_selection, \
                param_for_main_selection, \
                param_for_2nd_chance_selection, \
                BGC_stats, \
                product_stats, \
                path_of_stats_dir ):
    """
    Plot statistics of BGC-selection and product(s) of selected BGCs.

    Parameters
    ----------
    param_for_preliminary_selection     : dict of {str : str}
        Parameter for preliminary selection, i.e. minimum number of core genes.
    param_for_main_selection            : dict of {str : str}
        Parameters for main selection, i.e. minimum length of cluster (in bp), minimum distance of each core gene to edges of cluster (in bp) and minimum number of additional biosynthetic genes.
    param_for_2nd_chance_selection      : dict of {str : str}
        Parameter for second-chance selection, i.e. minimum number of additional biosynthetic genes.
    BGC_stats                           : dict of {str : int}
        Statistics of BGC-selection.
    product_stats                       : dict of {str : int}
        Statistics of product(s) of selected BGCs.
    path_of_stats_dir                   : str
        Path of directory that will contain all statistics results for task 2.

    Returns
    -------
    None.

    Output files
    ------------
    Two image files of plot of BGC-statistics and product statistics.
    """
    # # -----------Get a range with customized maximum value and step for axis-----------------------
    def customize_distance_btw_ticks_and_limit_of_axis(DataFrame):
        """
        Returns a range with a commonly used distance between two ticks (e.g. 10, 20, 25, etc.) and an overrated maximum value (this range will be used for making an axis of a plot).

        Parameters
        ----------
        DataFrame : a pandas DataFrame

        Returns
        -------
        A range with a commonly used distance between two ticks (e.g. 10, 20, 25, etc.) and an overrated maximum value.
        """
        # Note: this function is used only in this module and it returns a commonly used distance between ticks of axis and an "overrated" maximum value on axis of plots.
        max_value = int( DataFrame.max().max() ) # Get maximum value of axis (e.g. number of all analyzed BGCs or highest product frequency)

        Nmin_ticks_on_axis = 5 # Minimum number of ticks on axis in plots (default = 5)

        if max_value < Nmin_ticks_on_axis: # Case 1: max_value < 5
            return range(0, max_value + 4, 1)
        elif max_value < Nmin_ticks_on_axis * 2: # Case 2: 5 <= max_value < 10
            return range(0, max_value + 8, 2)
        else: # Case 3: max_value >= 10
            distances_between_two_ticks = [2, 4, 5, 10, 20, 25, 50, 100, 150, 200, 250, 500, 1000, 2000, 2500, 5000, 10000] # List of some commonly used distances between ticks on axis.
            distances_between_two_ticks.reverse() # In order to find the biggest distance in the list that is smaller than max_value/Nmin_ticks_on_axis.
            for distance in distances_between_two_ticks:
                if max_value/Nmin_ticks_on_axis >= distance:
                    return range(0, max_value + int(max_value/Nmin_ticks_on_axis)*3, distance) # "max_value + int(max_value/Nmin_ticks_on_axis)*3", "max_value + 4" and "max_value + 8" ensure that there is enough space for legend and a note text above the bars in the plot.
    # # -----------Get a range with customized maximum value and step for axis-----------------------

    # # -----------Set global configurations for plots-----------------------
    plt.rcParams['xtick.labelsize']=20 # Set size of labels of ticks on x-axis
    plt.rcParams['ytick.labelsize']=20 # Set size of labels of ticks on y-axis
    font_of_label = {'family': 'serif', 'color':  'darkred', 'weight': 'normal', 'size': 25} # Set font style of labels for x- and y-axes.
    # # -----------Set global configurations for plots-----------------------

    # # -----------Create a note for plots (optional)-----------------------
    note = r"Preliminary selection: number of core biosynthetic genes $\geqslant$ " + param_for_preliminary_selection["Minimum number of core genes"] + "\n" + \
           r"Main selection: length of cluster $\geqslant$ " + "{:,}".format(int(param_for_main_selection["Minimum length (in bp)"])) + " bp; distance of each core gene to both edges $\geqslant$ " + "{:,}".format(int(param_for_main_selection["Minimum distance (in bp)"])) + " bp; number of additional genes $\geqslant$ " + param_for_main_selection["Minimum number of additional biosynthetic genes"] + "\n" + \
           r"Second-chance selection: number of additional genes $\geqslant$ " + param_for_2nd_chance_selection["Minimum number of additional biosynthetic genes"]
    # # -----------Create a note for plots (optional)-----------------------

    # # -----------Plot statistics of BGC-selection-----------------------
    DataFrame_of_BGC_stats = pd.DataFrame(BGC_stats, index=[""])
    plot_of_BGC_stats      = DataFrame_of_BGC_stats.plot(kind="bar", figsize=(12,10), zorder=2.0) # Make bar plot of statistics for BGC-selection.
    for i in range(len(BGC_stats)):
        plot_of_BGC_stats.bar_label(plot_of_BGC_stats.containers[i], label_type='edge', fontsize=15, zorder=2.0) # Add corresponding y-values (labels) on each bar of plot.
    if side_options.add_note_to_plot == True:
        plt.figtext(0.09, 0.83, note, wrap=True, horizontalalignment='left', fontstyle='italic', fontsize=9.5, zorder=2.0) # Add a note (created above) to plot (this is optional).
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=3, fancybox=True, fontsize=20) # Set position of legend box ("ncol=3", i.e. three columns in legend box, because there are three entries in statistics for BGC-selection).
    plt.xticks([]) # No ticks on x axis for this plot
    plt.yticks(customize_distance_btw_ticks_and_limit_of_axis(DataFrame_of_BGC_stats))
    # In this plot: no label is needed for x-axis as there are no numerical values on x-axis and the legend should be enough to explain the bars on x-axis.
    plt.ylabel(ylabel="Number of BGCs", fontdict=font_of_label)
    # plt.title(label="Results of BGC-selection", fontdict=font_of_label) # Optional.
    plt.grid(which='major', axis='y', alpha=1.0, linewidth=0.5, zorder=-3.0) # Add grid lines parallel to x-axis on plot.
    plt.tight_layout() # Adapt margin around graph so that all labels on x- and y- axis are not truncated.
    plt.savefig(path_of_stats_dir + names_and_paths.name_of_plot_of_BGC_statistics) # Note: after "plt.savefig()" here (or also "plt.show()"), all next statistics will be plotted on new plot (and not on the same saved plot).
    # # -----------Plot statistics of BGC-selection-----------------------

    # # -----------Group or sort all product(s) before plotting------------------
    if product_stats != {}: # Only sort if at least one product of selected BGCs is present.
        if side_options.group_products_in_predefined_groups == True:
            product_stats = stats_utils.group_products(product_stats) # Optional: group all products (of selected BGCs) in predefined groups.
        else:
            product_stats = dict(sorted(product_stats.items(), key=lambda x: x[1], reverse=False)) # Sort products according to their frequencies. Note: "product_stats" is a dict Object, not a list; .items() returns a list of tuples of key:value which "sorted()" can be applied on; x[1] means sorting according to values, i.e. frequency of products.
    # # -----------Group or sort all product(s) before plotting------------------

    # # -----------Plot product(s) of selected BGCs-----------------------
    if product_stats != {}: # Only make plot for all products if there is at least one product of selected BGCs.
        DataFrame_of_product_stats              = pd.DataFrame(product_stats, index=[""]).T # Make transposed DataFrame for horizontal bar plot.
        colors_for_bars, patterns_for_bars      = stats_utils.make_lists_of_colors_and_patterns_for_bars(product_stats) # Make color and pattern for each bar on plot.
        plot_of_product_stats                   = DataFrame_of_product_stats.plot(kind="barh", figsize=(12,10), legend=None, zorder=2.0) # Make plot of statistics for products of selected BGCs. Note: "barh" enables horizontal bar chart, and "zorder" for drawing bars above the grid lines created by "plt.grid()" (see below).
        for i in range(1): # range(1) because of transpose T on DataFrame
            plot_of_product_stats.bar_label(plot_of_product_stats.containers[i], label_type='edge', fontsize=15, zorder=2.0) # Add corresponding y-values (labels) on each bar of plot.
        for patch, color, pattern in zip(plot_of_product_stats.patches, colors_for_bars, patterns_for_bars):
            patch.set_facecolor(color)          # Assign corresponding color to bar.
            patch.set_hatch(pattern)            # Assign corresponding pattern to bar.
            patch.set_edgecolor("black")        # Color of pattern contour.
            patch.set_linewidth(0.8)            # Line width of pattern contour (?).
        if side_options.fill_background_plot_with_grey == True:
            plot_of_product_stats.patch.set_facecolor('grey') # Set background color to "grey" for better contrast.
            plot_of_product_stats.patch.set_alpha(0.5) # Set blending degree of background color.
        if side_options.add_note_to_plot == True:
            plt.figtext(0.9, 0.1, note, wrap=False, horizontalalignment='left', rotation=-90, fontstyle='italic', fontsize=9.5, zorder=2.0) # Add a note (created above) to plot (optional)
        # plt.xticks(range(0, 91, 10)) # Only use for bachelor project to create plots with same defined x range, customized for eased comparison between plots. In general usage, the command below for "xticks" should be out-commented and put in used.
        plt.xticks(customize_distance_btw_ticks_and_limit_of_axis(DataFrame_of_product_stats))
        plt.xlabel(xlabel="Selected BGCs", fontdict=font_of_label)
        plt.ylabel(ylabel="Product classes", fontdict=font_of_label)
        # plt.title(label="Products of selected BGCs", fontdict=font_of_label) # Optional
        plt.grid(which='major', axis='x', alpha=1.0, linewidth=0.5, zorder=-3.0) # Add grid lines parallel to y-axis on plot
        plt.tight_layout() # Adapt margin around graph so that all labels on x- and y- axis are not truncated.
        plt.savefig(path_of_stats_dir + names_and_paths.name_of_plot_of_product_statistics) # Note: after "plt.savefig()" here (or also "plt.show()"), next statistics will be plotted on new plot (and not on the same saved plot).
        if side_options.show_plots == True:
            plt.show() # Optional: by True show at once all plots made until here (all plots made since the last command "plt.show()", which could also be saved previously). Beware of interruption!
    # # -----------Plot product(s) of selected BGCs-----------------------
# # -----------Make plots for statistics-----------------------


# # -----------Create statistics file-----------------------
def make_stats_file( param_for_preliminary_selection, \
                     param_for_main_selection, \
                     param_for_2nd_chance_selection, \
                     BGC_stats, \
                     product_stats, \
                     path_of_stats_dir ):
    """
    Make a statistics file that contains results of BGC-selection and product(s) of selected BGCs.

    Parameters
    ----------
    param_for_preliminary_selection     : dict of {str : str}
        Parameter for preliminary selection, i.e. minimum number of core genes.
    param_for_main_selection            : dict of {str : str}
        Parameters for main selection, i.e. minimum length of cluster (in bp), minimum distance of each core gene to edges of cluster (in bp) and minimum number of additional biosynthetic genes.
    param_for_2nd_chance_selection      : dict of {str : str}
        Parameter for second-chance selection, i.e. minimum number of additional biosynthetic genes.
    BGC_stats                           : dict of {str : int}
        Statistics of BGC-selection.
    product_stats                       : dict of {str : int}
        Statistics of product(s) of selected BGCs.
    path_of_stats_dir                   : str
        Path of directory that will contain all statistics results for task 2.

    Returns
    -------
    None.

    Output files
    ------------
    A statistics file containing results of BGC-selection and product(s) of selected BGCs.
    """
    stats_file = open(path_of_stats_dir + names_and_paths.name_of_statistics_file, "w")

    # # -----------Write time of analysis into file-----------------------
    stats_file.write(">>> Analysis finished at: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n\n")
    # # -----------Write time of analysis into file-----------------------

    # # -----------Write used parameters into file-----------------------
    stats_file.write(">>> Parameters used for selection:\n")
    stats_file.write(">> For preliminary selection:"    + pd.DataFrame(param_for_preliminary_selection, index = [""]).T.to_string() + "\n")
    stats_file.write(">> For main selection:"           + pd.DataFrame(param_for_main_selection, index = [""]).T.to_string() + "\n")
    stats_file.write(">> For second-chance selection:"  + pd.DataFrame(param_for_2nd_chance_selection, index = [""]).T.to_string() + "\n\n")
    # # -----------Write used parameters into file-----------------------

    # # -----------Write statistics (BGCs and the product(s) of selected BGCs)-----------------------

    # # -----------Write statistics of BGC-selection-----------------------
    if BGC_stats["All BGCs"] > 0:
        DataFrame_of_BGC_stats                    = pd.DataFrame(BGC_stats, index=[""]) # Make DataFrame of BGC statistics. This is needed for adding the new row "Percentages" (see below).
        DataFrame_of_BGC_stats.loc["Percentages"] = [ "{:.2%}".format( DataFrame_of_BGC_stats.iloc[0,i] / DataFrame_of_BGC_stats.iloc[0,2] ) for i in range(len(BGC_stats)) ] # Before printing out: add a row for percentages to DataFrame ("DataFrame_of_BGC_stats.iloc[0,2]" = "All BGCs" = Number of all analyzed BGCs)
        stats_file.write(">>> Results of BGC-selection:\n" + DataFrame_of_BGC_stats.to_string(index = False) + "\n\n")
    else:
        stats_file.write("> No BGC was found!\n\n")
    # # -----------Write statistics of BGC-selection-----------------------

    # # --------------Sort and group all found product(s) before writing to file------------------
    if product_stats != {}: # Only sort if at least one product of selected BGCs is present
        if side_options.group_products_in_predefined_groups == True:
            product_stats = stats_utils.group_products(product_stats) # Optional: group all found products (of selected BGCs) in predefined groups.
        else:
            product_stats = dict(sorted(product_stats.items(), key=lambda x: x[1], reverse=False)) # Sort products according to their frequencies. Note: "product_stats" is a dict Object, not a list; .items() returns a list of tuples of key:value which "sorted" can be applied on; x[1] means sorting according to values, i.e. frequency of products.
    # # --------------Sort and group all found product(s) before writing to file------------------

    # # -----------Write products of selected BGCs-----------------------
    if product_stats != {}:
        DataFrame_of_product_stats = pd.DataFrame(product_stats, index=[""])
        stats_file.write(">>> Product(s) of selected BGCs:\n" + DataFrame_of_product_stats.to_string(index = False) + "\n\n")
    else:
        stats_file.write("> No BGC was selected and therefore no product of selected BGCs!\n\n") # Note: if there is no product of selected BGCs, then there was no BGC selected.
    # # -----------Write products of selected BGCs-----------------------

    # # -----------Write statistics (BGCs and the product(s) of selected BGCs)-----------------------

    stats_file.close()
# # -----------Create statistics file-----------------------
