''' This module contains utility functions that help visualize the plots of statistics in an optimal way: the first function groups all detected products belonging to corresponding classes of biosynthetic products so as to simplify the
    plots of product statistics, while the second function assigns the bars on the plots for product(s) of selected BGCs unique colors and patterns, thereby highlighting them on the plot, and also making them distinguishable. '''


import random


# # -----------Group products that are similar/belong to the same class of products-----------------------
def group_products(product_stats):
    """
    Group products that belong to the same class.

    Parameters
    ----------
    product_stats : dict of {str : int}
        Statistics of product(s) of selected BGCs.

    Returns
    -------
    product_stats_grouped : dict of {str : int}
        Statistics of product(s) of selected BGCs where products belonging to same class are grouped and represented by the class (occurrence frequency of each class is sum of that of its member product(s)).
    """
    list_of_predefined_groups_of_products = ["hybrid", "others", "RiPP", "NRPS-like", "T1PKS", "NRPS", "arylpolyene", "T3PKS", "terpene"] # Note: this list can be updated by user. Also, the order of the product groups in this list is also the order of the product groups for printing out on Terminal, plotting and writing in file. Important: the groups "others", "hybrid" should always be in this list.
    product_stats_grouped                 = dict.fromkeys(list_of_predefined_groups_of_products, 0)
    for product in product_stats:
        if   product in list_of_predefined_groups_of_products:                                                  # Predefined groups of products that should only be plotted
            product_stats_grouped[product]   += product_stats[product]
        elif "+" in product:                                                                                    # Hybrid BGCs contain "+" in their names
            product_stats_grouped["hybrid"]  += product_stats[product]
        elif product in ["RRE-containing", "LAP", "lanthipeptide-class-i", "lanthipeptide-class-ii", "lanthipeptide-class-iii", "lanthipeptide-class-iv", "thiopeptide"]:                     # Products from class RiPP
            product_stats_grouped["RiPP"]    += product_stats[product]
        else:                                                                                                   # Products that do not belong to any predefined groups
            product_stats_grouped["others"]  += product_stats[product]
    return  product_stats_grouped
    # Note: use here the operator "+=" instead of "=" to ensure only the specified keys are created and their values in the dictionary.
# # -----------Group products that are similar/belong to the same class of products-----------------------


# # -----------Make lists of colors and patterns for bars on plot-----------------------
def make_lists_of_colors_and_patterns_for_bars(product_stats):
    """
    Make two lists, one contains colors and the other contains patterns for the bars that represent product(s) on plot (each bar has different combination of color and pattern).

    Parameters
    ----------
    product_stats : dict
        Statistics of product(s) of selected BGCs.

    Returns
    -------
    colors_for_bars : list of str
        A list that contains the colors for the bars representing the product(s) on the plot.
    patterns_for_bars : list of str
        A list that contains the patterns for the bars representing the product(s) on the plot.
    """
    number_of_products = len(product_stats)

    # # -----------Define all available colors and patterns-----------------------
    all_colors             = ["blue", "green", "red", "cyan", "magenta", "yellow", "grey", "orange"] # All available colors that can be applied on bars of plots.
    number_of_all_colors   = len(all_colors)
    all_patterns           = ["|", "\\", "/", "+", "-", ".", "*", "x", "o"]                          # All available patterns that can be applied on bars of plots.
    number_of_all_patterns = len(all_patterns)
    # # -----------Define all available colors and patterns-----------------------

    reserve_colors_for_bars   = all_colors   * (number_of_products // number_of_all_colors)   + all_colors[  : (number_of_products % number_of_all_colors)   ] # Not so necessary: create a list of (repeating) colors with length = number of all products
    reserve_patterns_for_bars = all_patterns * (number_of_products // number_of_all_patterns) + all_patterns[: (number_of_products % number_of_all_patterns) ] # Not so necessary: create a list of (repeating) patterns with length = number of all products

    # # -----------Make assignment scheme: product -> (color, pattern)-----------------------
    colors_and_patterns_assignment_scheme =    { "RiPP"                             : ("green", "+"),
                                                 "NAPAA"                            : ("green", "|"),
                                                 "NRPS"                             : ("orange", "\\"),
                                                 "NRPS-like"                        : ("orange", "*"),
                                                 "T1PKS"                            : ("red", "/"),
                                                 "T3PKS"                            : ("red", "|"),
                                                 "acyl_amino_acids"                 : ("magenta", "*"),
                                                 "arylpolyene"                      : ("red", "-"),
                                                 "betalactone"                      : ("orange", "."),
                                                 "hglE-KS"                          : ("grey", "+"),
                                                 "lanthipeptide-class-iv"           : ("cyan", "/"),
                                                 "phosphonate"                      : ("magenta", "+"),
                                                 "terpene"                          : ("yellow", "."),
                                                 "thiopeptide"                      : ("green", "-"),
                                                 "others"                           : ("black", "\\"),
                                                 "hybrid"                           : ("black", ".") }
                                                 # Note: the assignment is bijective as long as number_of_products <= SCM(number_of_all_colors, number_of_all_patterns) (SCM: smallest common multiple)
                                                 # Important: the keys "others" and "hybrid" should always be considered in this scheme!
                                                 # Note: this assignment scheme should be adapted when use different input sequence data!
                                                 # Note: the order of the keys in this scheme must not necessarily match the order in the list of predefined groups of products.
    # # -----------Make assignment scheme: product -> (color, pattern)-----------------------

    # # -----------Create lists containing colors and patterns for bars of plots-----------------------
    colors_for_bars   = []
    patterns_for_bars = []
    for product in product_stats:
        if product in colors_and_patterns_assignment_scheme:
            colors_for_bars.append(colors_and_patterns_assignment_scheme[product][0])    # Assign the corresponding color to the bar representing the product, if product is defined in scheme.
            patterns_for_bars.append(colors_and_patterns_assignment_scheme[product][1])  # Assign the corresponding pattern to the bar representing the product, if product is defined in scheme.
        else:
            colors_for_bars.append(random.choice(all_colors))                            # Assign a random color to the bar representing the product, if product is not defined in scheme.
            patterns_for_bars.append(random.choice(all_patterns))                        # Assign a random pattern to the bar representing the product, if product is not defined in scheme.
    # # -----------Create lists containing colors and patterns for bars of plots-----------------------

    return colors_for_bars, patterns_for_bars
# # -----------Make lists of colors and patterns for bars on plot-----------------------
