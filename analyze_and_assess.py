''' This module has a function that takes in the read content of a Genbank antiSMASH-output file for a single BGC, finds and collects relevant data from the content,
    uses these data to examine the selection criteria and decides the selection result for the query BGC. The selection result is stored in the variable "selection_status_for_BGC" and is output by the function for the further usage by other downstream module.
    A scheme of the selection algorithm can be found in the directory "info". This module also stores "textual tags" that can be used to find corresponding information (see list below). '''


import re # Necessary!


# # --------------Text strings used for data extraction----------------
# Declaration of text strings (in easy-to-read form) that are used below for data mining (below, some of these are combined with regular expressions)

delimiter_btw_data_of_genes_and_DNA_seq_of_whole_BGC                    = "ORIGIN\n"  # Note: "\n" for avoiding the string "ORIGIN" that might occur somewhere else, e.g. in name of BGC.
delimiter_btw_CDS_blocks                                                = "   CDS   " # Note: trailing and leading spaces in string for avoiding the string "CDS" that might occur somewhere else, e.g. in name of BGC or in an amino acid sequence.

# # Textual tags for searching text fields that contain gene- and BGC-related data:
# text_tag_for_gene_kind                                                = "gene_kind="
# text_tag_for_locus_of_gene                                            = "locus_tag="
# text_tag_for_aa_seq                                                   = "translation="
# text_tag_for_name_of_BGC                                              = "DEFINITION"
# text_tag_for_product_of_BGC                                           = "/gene_functions="biosynthetic (rule-based-clusters)"

# # Textual tags for searching text fields that contain data for the following gene types:
# text_tag_for_core_genes                                               = "biosynthetic"
# text_tag_for_additional_genes                                         = "biosynthetic-additional"
# text_tag_for_transport_genes                                          = "transport"
# text_tag_for_regulatory_genes                                         = "regulatory"
# text_tag_for_resistance_genes                                         = "resistance"

# unambiguous_nucleotide                                                = "n"
# unambiguous_aa                                                        = "X"

label_for_file_of_one_BGC                                               = "NOTE: This is a single cluster extracted from a larger record!"
# # --------------Text strings used for data extraction----------------


def analyze_and_assess_BGC(content, param_for_preliminary_selection, param_for_main_selection, param_for_2nd_chance_selection):
    """
    Find, extract and store relevant data of a query BGC and its gene(s) (only core and additional biosynthetic genes) from the content of its Genbank (.gbk) file, then use these data to assess the query BGC.

    Parameters
    ----------
    content                             : str
        Content of a Genbank (.gbk) file for a BGC.
    param_for_preliminary_selection     : dict of {str : str}
        Parameter for preliminary selection, i.e. minimum number of core genes.
    param_for_main_selection            : dict of {str : str}
        Parameters for main selection, i.e. minimum length of cluster (in bp), minimum distance of each core gene to edges of cluster (in bp) and minimum number of additional biosynthetic genes.
    param_for_2nd_chance_selection      : dict of {str : str}
        Parameter for second-chance selection, i.e. minimum number of additional biosynthetic genes.

    Returns
    -------
    info_of_BGC                 : dict of {str : str}
        General information of BGC: name of BGC, length of BGC (in bp) and product(s) of BGC.
    selection_status_for_BGC    : str
        Selection result of BGC: either "discarded", "passed main selection" or "passed second-chance selection".
    """
    # # --------------Get values for parameters----------------
    min_num_of_core_genes                                       = param_for_preliminary_selection["Minimum number of core genes"]

    min_length                                                  = param_for_main_selection["Minimum length (in bp)"]
    min_distance                                                = param_for_main_selection["Minimum distance (in bp)"]
    min_num_of_additional_genes_for_main_selection              = param_for_main_selection["Minimum number of additional biosynthetic genes"]

    min_num_of_additional_genes_for_2nd_chance_selection        = param_for_2nd_chance_selection["Minimum number of additional biosynthetic genes"]
    # # --------------Get values for parameters----------------

    splitted_content = content.split(delimiter_btw_data_of_genes_and_DNA_seq_of_whole_BGC) # Split the content of the file at "ORIGIN" (which is the text between data of genes and the DNA sequence of whole BGC) and return a list of two elements. The first element is a string that contains the CDS blocks of all gene(s), the second element is a string that contains the DNA sequence of the BGC.

    # # --------------Extract DNA sequence of BGC----------------
    DNA_seq_of_BGC = splitted_content[1].replace("\n", "").lower() # Get the second element of the list "splitted_content", which is the DNA sequence of BGC.
    # # --------------Extract DNA sequence of BGC----------------

    # # --------------Extract general information of BGC----------------
    data_of_all_genes = splitted_content[0] # Get the first element of the list "splitted_content", which contains the CDS blocks of all gene(s).

    info_of_BGC = {}

    # Use try...except... blocks here to skip extracting data for query BGC in case one of the following types of information is not readable:
    try:
        name_of_BGC     = re.search("DEFINITION([^\n]*)\n", data_of_all_genes).group(1).strip() # Note: the (unique) field "DEFINITION" always contains the full name of the BGC (with possibly the length (in bp) of it). With the string method ".strip()", the extracted name does not contain any leading/trailing spaces (for better readability).
    except:
        name_of_BGC     = None # If name of BGC cannot somehow be read
    try:
        length_of_BGC   = re.search("\s\s\s([0-9]+)\s(bp){1}", data_of_all_genes).group(1) # Return the first matching string of form: space*3 + any number + space + "bp" (the three spaces separate the length from the name of BGC). The method ".group(1)" retrieves only the numeric part.
    except:
        length_of_BGC   = 0   # If length of BGC cannot somehow be read
    try:
        products_of_BGC = list( set( [product.replace("\n", "").strip() for product in re.findall("/gene_functions=\"biosynthetic \(rule-based-clusters\)([^:]*):", data_of_all_genes)] ) ) # "set()" to eliminate duplicates, at the end a list of (nonduplicate) product(s) will be returned. Note: re.findall(pattern, text) returns the matching substring defined by the capturing group (...) (if there is such a group in the pattern) so .group() is not needed to extract to matching substring.
                                                                                                                                                                                            # Note: the field "/product="..."" sometimes can contain unrelated or specific information about the product(s) of the BGC, whereas the information in the field "/gene_functions="biosynthetic (rule-based-clusters) ..." always contains general information (i.e., class(es) of products) that suffices the selection procedure.
        products_of_BGC.sort() # All products in the list should be sorted in a certain order, so that all hybrids with the same constituent products will have identical lists of products. (Note: this method has to be executed separated from the above code, e.g. in a new line!)
    except:
        products_of_BGC = [] # In case the BGC has no product or data for the product(s) is incompatible, assign an empty list (in most cases this is equivalent to the case where the BGC has no annotated core biosynthetic gene).

    info_of_BGC["Name of BGC"]             = name_of_BGC
    info_of_BGC["Length of BGC (in bp)"]   = length_of_BGC
    info_of_BGC["Product(s) of BGC"]       = products_of_BGC
    # # --------------Extract general information of BGC----------------

    # # --------------Define function for finding, extracting and storing relevant data for a gene kind in BGC----------------

    def extract_and_store_data_for_a_gene_kind(content, gene_kind, data_record_for_gene_kind):
        # # --------------Identify all fields containing data for the given gene kind----------------
        CDS_blocks_for_gene_kind = [ CDS_block for CDS_block in data_of_all_genes.split(delimiter_btw_CDS_blocks) if ("/gene_kind=\"" + gene_kind + "\"") in CDS_block ] # "delimiter_btw_CDS_blocks" = "   CDS   " (defined above).
                                                                                                                                                                         # Split content of file at each occurrence of "   CDS   " and keep only the CDS blocks with data to given "gene_kind". Spaces in the searching pattern ("   CDS   ") are important! (So that unrelated fields such as translations, i.e. protein sequences that happen to contain "CDS", will not be splitted as well, allowing the whole CDS blocks to be each obtained).
                                                                                                                                                                         # Due to the "if" condition in the list comprehension, the list "CDS_blocks_for_gene_kind" contains as many elements as the CDS blocks for the given gene kind in file content.
        # # --------------Identify all fields containing data for the given gene kind----------------

        # # --------------Extract needed data of given gene kind----------------
        if len(CDS_blocks_for_gene_kind) > 0: # Only proceed to extract data for the given gene kind if this list has at least 1 element, i.e. contains at least one CDS block for gene kind. In case no CDS block for gene kind is present in "content", this list would be an empty list, i.e. [].
            for block in CDS_blocks_for_gene_kind:
                try:
                    locus_of_gene        = re.search("/locus_tag=\"([^\"]*)\"", block).group(1)                                          # Search for the first "locus_tag" entry in the CDS block and extract from it the locus of gene (".group(1)" returns the matching substring defined by the capturing group in parentheses).
                    position_of_gene     = re.search("[0-9]+\.\.[0-9]+", block).group(0).split("..")                                     # Search in the CDS block for the first match and returns a list (with ".split()"): [start position, end position] (.group(0) returns the whole matching string).
                    translation_of_gene  = re.search("/translation=\"([A-Z\n\s]*)\"", block).group(1).replace("\n", "").replace(" ", "") # Return (with "re.search()") the (first matching) translation in the CDS block for the gene (".group(1)" returns only the translation part without the string "/translation="...""). Note: in each CDS block for each gene, the first occurring translation is always the complete translation of the gene. Last two ".replace()" methods for removing "\n" and spaces (for readability).
                except:
                    continue # Skip to next block when only one type of information (locus, position, translation) about the gene in current block is insufficient/has incompatible format (treated as if the gene was not there), because further examination for this gene would be impossible.
        # # --------------Extract needed data of given gene kind----------------

        # # --------------Store extracted data in given record----------------
                data_record_for_gene_kind.append(
                {
                    "locus"         : locus_of_gene,
                    "position"      : position_of_gene,
                    "translation"   : translation_of_gene
                }
                ) # Only executed if block "try" was executed successfully. Otherwise, if block "except" was executed, these code lines will be skipped.
        # # --------------Store extracted data in given record----------------

    # # --------------Define function for finding, extracting and storing relevant data for a gene kind in BGC----------------

    # # --------------Define data records for storing data of gene kinds----------------
    data_record_for_core_genes                  = []
    data_record_for_additional_genes            = []
    # data_record_for_transport_genes           = [] # not so necessary
    # data_record_for_regulatory_genes          = [] # not so necessary
    # data_record_for_resistance_genes          = [] # not so necessary
    # Note: assume at the beginning that there is no record for each of these gene kinds in file content (i.e. each list is empty at the beginning).
    # # --------------Define data records for storing data of gene kinds----------------

    # # --------------Extract and store data for specified gene kinds in BGC----------------
    extract_and_store_data_for_a_gene_kind(content, gene_kind = "biosynthetic", data_record_for_gene_kind = data_record_for_core_genes)
    extract_and_store_data_for_a_gene_kind(content, gene_kind = "biosynthetic-additional", data_record_for_gene_kind = data_record_for_additional_genes)
    # extract_and_store_data_for_a_gene_kind(content, gene_kind = "transport", data_record_for_transport_genes)   # not necessary
    # extract_and_store_data_for_a_gene_kind(content, gene_kind = "regulatory", data_record_for_regulatory_genes) # not necessary
    # extract_and_store_data_for_a_gene_kind(content, gene_kind = "resistance", data_record_for_resistance_genes) # not necessary
    # # --------------Extract and store data for specified gene kinds in BGC----------------

    # # --------------Check selection criteria and select if fulfilled or discard if not----------------
    selection_status_for_BGC     = "discarded" # Define variable that will contain selection result for BGC (assume at the beginning that BGC does not pass any selection round). This variable will store at the end of analysis for BGC only one of three results: "passed main selection", "passed second-chance selection" or "discarded".

    # # --------------Preliminary selection----------------
    if len(DNA_seq_of_BGC) == 0 or len(info_of_BGC["Product(s) of BGC"]) == 0 or len(data_record_for_core_genes) < int(min_num_of_core_genes):
        selection_status_for_BGC = "discarded"
    elif "n" in DNA_seq_of_BGC:
        selection_status_for_BGC = "discarded"
    else:
        for gene in (data_record_for_core_genes + data_record_for_additional_genes): # Merge two lists together for examination:
            if "X" in gene["translation"]:
                selection_status_for_BGC = "discarded"
                break
            else:                                                                    # First, query BGC is checked whether it has a nonempty DNA sequence and at least one annotated product.
                selection_status_for_BGC = "passed preliminary selection"            # Then preliminary selection: query BGC must fulfill here three criteria: it should (1) carry at least as many core genes as required by user, and (2 & 3) must not have any ambiguous nucleotide ("n") in its whole DNA sequence or ambiguous amino acid ("X") in translation of core and additional genes.
    # # --------------Preliminary selection----------------

    # # --------------Main & second-chance selection----------------
    if selection_status_for_BGC == "passed preliminary selection":
        if int(info_of_BGC["Length of BGC (in bp)"]) >= int(min_length) \
            and int(data_record_for_core_genes[0]["position"][0]) >= int(min_distance) \
                and int(info_of_BGC["Length of BGC (in bp)"]) - int(data_record_for_core_genes[-1]["position"][1]) >= int(min_distance) \
                    and len(data_record_for_additional_genes) >= int(min_num_of_additional_genes_for_main_selection):
                        selection_status_for_BGC = "passed main selection"                              # Main selection: query BGC must fulfill 3 criteria: (1) its sequence length must exceed the user-defined parameter (stored in variable "min_length"), (2) the distance of each core gene to both (left and right) edges must exceed the user-defined parameter (stored in variable "min_distance")...
                                                                                                        # ... and (3) its number of additional genes must exceed the user-defined parameter (stored in "min_num_of_additional_genes_for_main_selection").
        elif len(data_record_for_additional_genes) >= int(min_num_of_additional_genes_for_2nd_chance_selection):
                        selection_status_for_BGC = "passed second-chance selection"                     # Second-chance selection: in case the query BGC fails the main selection, it can still be further examined by checking only one criterion: its number of additional genes must exceed the user-defined parameter (stored in "min_num_of_additional_genes_for_2nd_chance_selection"). This is similar to (3) in main selection but...
                                                                                                        # ... a higher number of additional genes is required here because this selection round is supposed to be stricter (to make sure the query BGC, if selected, could still be an intact and functional one even if it does not pass the main selection). If this stricter criterion is fulfilled, query BGC can still be selected.
        else:
                        selection_status_for_BGC = "discarded"                                          # Here, the query BGC passed the preliminary selection, but neither the main nor the second-chance selection, and will therefore be discarded (the result is the same as for query BGCs that did not pass the preliminary selection at the beginning, which are also discarded).
    # # --------------Main & second-chance selection----------------
    # # --------------Check selection criteria and select if fulfilled or discard if not----------------

    return info_of_BGC, selection_status_for_BGC
