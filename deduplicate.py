''' This module contains a function that takes in a list of paths of files, e.g. input files for antiSMASH, and attempts to process this list so that at the end, all files in this list have unique name, by removing and/or renaming files with duplicate name (this e.g. can reduce execution time of a task with given input files). '''


import re

import names_and_paths
import side_options


# # -----------Remove or rename files with duplicate name in given list-----------------------
def remove_or_rename_files_with_duplicate_name(paths):
    """
    Remove or rename files that have same name in a given list of paths of files (e.g. input files for a task).

    Parameters
    ----------
    paths : list of str
        A list of path(s) of file(s) (e.g. input file(s) for a task).

    Input files
    -----------
    None.

    Returns
    -------
    The given list with no files having duplicate name (the paths of these files in the given list have been removed or renamed/changed).

    Output files
    ------------
    None.
    """
    # # -----------Compare content of two given files-----------------------

    def compare_content_of_two_files(path_of_file1, path_of_file2):
        """
        Compare content of two given files (this function is used only by the outer function).

        Parameters
        ----------
        path_of_file1 : str
            Path of first file (e.g. a .fasta or a .gbk file).
        path_of_file2 : str
            Path of second file (e.g. a .fasta or a .gbk file).

        Returns
        -------
        str
            Result of content comparison for the two files: either "different content" or "(almost) identical content" (which will be further used by the outer function).

        Output files
        ------------
        None.
        """
        # # -----------Make a list of lines for each file-----------------------
        with open(path_of_file1) as file_obj1, open(path_of_file2) as file_obj2:
            list_of_lines1 = file_obj1.readlines()
            list_of_lines2 = file_obj2.readlines()
        # # -----------Make a list of lines for each file-----------------------

        # # -----------Compare numbers of lines of both files (quick comparison)-----------------------
        if abs(len(list_of_lines1) - len(list_of_lines2)) > 20:
            return "different content"
        # # -----------Compare numbers of lines of both files (quick comparison)-----------------------

        # # -----------Compare line by line of both files, if they differ less than 20 lines-----------------------
        else:
            num_of_different_lines = 0
            for line_number in range( min(len(list_of_lines1), len(list_of_lines2)) ):
                if list_of_lines1[line_number] != list_of_lines2[line_number]:
                    num_of_different_lines += 1

                if num_of_different_lines > 50:
                    return "different content" # In case more than 50 different lines are found, stop comparing lines of files here and return result of comparison of the two files, in this case "different content".

            return "(almost) identical content" # In case at the of the loop only less than 50 different lines are found, return this result. Note: for two actually identical files, the different lines could be because of different version of used program/tool, date and time of analysis, etc.
        # Note: the difference of numbers of lines and "num_of_different_lines" are generally independent from each other.
        # # -----------Compare line by line of both files, if they differ less than 20 lines-----------------------

    # # -----------Compare content of two given files-----------------------


    paths_to_remove = [] # Define a list that will contain paths of files with duplicate name, if there are any in given list of file(s). which will be removed from given list.
    paths_to_rename = [] # Define a list that will contain paths of files with duplicate name, if there are any in given list of file(s), which will be renamed in given list.

    # # -----------Loop through list and compare every pair of two files and rename or remove one of them from list if they have duplicate name-----------------------
    for index1 in range(len(paths) - 1): # Note: in case given list only contains one path for one file, and hence there will be no files with duplicate name, this loop (and the other two after this) will not be executed.
        path_of_file1                   = paths[index1]
        name_of_file1                   = path_of_file1.split("/")[-1]  # Note: name of file is always behind the last slash in its path.
        name_of_file1_without_extension = re.sub("|".join(names_and_paths.file_extensions_of_antismash_inputfiles), "", name_of_file1) # Get name of file without file extension.
        for index2 in range(index1 + 1, len(paths)): # Loop through list and compare each file in this loop with the file of outer loop. IMPORTANT: this loop has to start from "index1" + 1! This is because all file(s) that this loop will go through were already compared with file(s) with index <= "index1".
            path_of_file2 = paths[index2]
            if path_of_file2 in paths_to_remove:
                continue # Skip examining file if file is (almost) identical to one of other files (found out in previous loop) and is going to be removed later.
            name_of_file2 = path_of_file2.split("/")[-1]
            name_of_file2_without_extension = re.sub("|".join(names_and_paths.file_extensions_of_antismash_inputfiles), "", name_of_file2) # Get name of file without file extension.

            if name_of_file2_without_extension == name_of_file1_without_extension: # In case found a file with duplicate name (name of file without extension should be used in comparison):

                if side_options.analyze_files_with_same_name_but_different_content == True: # In case files in given list with duplicate name are not to be skipped, but renamed (only their paths in given list are changed, but neither their actual names nor paths in system) if they have different content, or removed if they have identical content (until one file with the name is left in the list):
                    result_of_content_comparison = compare_content_of_two_files(path_of_file1, path_of_file2) # Compare the content of the files with duplicate name.
                    if result_of_content_comparison == "different content":
                        if not path_of_file2 in paths_to_rename: paths_to_rename.append(path_of_file2) # Add path of one of the two files with duplicate name, here "path_of_file2", to list of paths to be renamed (later) in case of different content. Note: check if path already exists in this list before adding to list, as otherwise the number of paths in this list would increase quickly.
                    elif result_of_content_comparison == "(almost) identical content":
                        if not path_of_file2 in paths_to_remove: paths_to_remove.append(path_of_file2) # Add path of one of the two files with duplicate name, here "path_of_file2", to list of paths to be removed (later) in case of (almost) identical content. Note: check if path already exists in this list before adding to list, as otherwise the number of paths in this list would increase quickly.
                    # Note: file that corresponds to "index1" with its name "name_of_file1" is kept as file with unique name in given list.

                elif side_options.analyze_files_with_same_name_but_different_content == False: # In case files in given list with duplicate name are to be all skipped, i.e. their paths will be removed from given list, regardless of content of the files:
                    if not path_of_file2 in paths_to_remove: paths_to_remove.append(path_of_file2) # Add path of one of the two files with duplicate name, here "path_of_file2", to list of paths to be removed (later). Note: check if path already exists in this list before adding to list, as otherwise the number of paths in this list would increase quickly.

            else:
                continue # Continue in case the two files have different names (content of the two files will not be compared in this case).

    for path in paths_to_remove:
        paths.remove(path) # Remove all path(s) of files with duplicate name, so that only one file is left with the unique name.

    for path_index in range(len(paths_to_rename)):
        old_path = paths_to_rename[path_index] # "old_path": path before renaming.
        new_path = old_path + (path_index + 1)*"_" + "renamed" # "new_path": path after renaming by adding the suffix "renamed" behind the file extension. Note: "path_index" + 1 because "path_index" starts at 0. With different number of "_" for each path, each "new_path" should be unique. File extension will not be at the end, but this is not a problem as later the original, correct path of file can be retrieved (e.g. with string methods).
        # new_path = old_path + "__renamed" + str(path_index) # Alternative: add a (random) numerical identifier as a (unique) suffix.
        try:
            paths.remove(old_path)
            paths.append(new_path) # Note: position where "new_path" is added in "paths" is not important.
            # Use try...except... block here because somehow some paths cannot be removed.
        except:
            print("\n> Cannot remove path of duplicate file: " + old_path) # Print path that cannot somehow be removed, so that user is informed that an identical file will be analyzed more than once. Care must then be taken when interpreting the statistics output at the end of task (e.g. due to overcounting a BGC)!
            pass # Skip if path cannot somehow be removed from list (this happens sometimes for some input files/folders, that is why a try...except... block is used here to skip this exception). Skipping such paths will only increase the execution time of task as possibly identical files will be analyzed (for task 2 particularly, the statistics will be falsified).

    return paths
    # IMPORTANT: do not remove or change element in a list, here path of an file, while looping through it! Instead, make a second list, e.g. a copy of the original list, for processing during the loop.
    # # -----------Loop through list and compare every pair of two files and rename or remove one of them from list if they have duplicate name-----------------------

# # -----------Remove or rename files with duplicate name in given list-----------------------
