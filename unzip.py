''' This module is responsible for unzipping all file(s) and/or folder(s) (only .zip format) in a directory of given path, more precisely, it replaces each zipped file/folder in the given directory with a folder that contains the zipped content. '''


import os
import zipfile

import names_and_paths


# # --------------Find and unzip all files/folders in specified directory---------------
def unzip_all_files_and_folders_in_dir(path_of_dir):
    """
    Unzip all zipped file(s)/folder(s) in the directory of given path.

    Parameters
    ----------
    path_of_dir : str
        Path of a directory.

    Returns
    -------
    None.

    Output folders
    --------------
    Folder(s), each replaces a zipped file/folder in directory of given path and contains its zipped content.
    """
    while True:
        found_zipped_file_or_folder = False # Assume at the beginning no zipped file or folder is found in directory with given path "path_of_dir".
        for dir, subdirs, files in os.walk(path_of_dir, topdown=True): # "os.walk()": loop through all folders and files in directory of given path "path_of_dir". "dir": absolute path of a certain directory found inside the directory of given path "path_of_dir", "subdirs": contains name(s) of subdirectory(-ies) in the directory "dir" (i.e. one level deeper than "dir"), "files": contains name(s) of file(s) in the directory "dir" (i.e. one level deeper than "dir").

            # # --------------Loop through all files in specified directory and search for all zipped files---------------

            for name_of_file in files:
                if name_of_file.endswith(".zip"):
                    found_zipped_file_or_folder = True # In case found a zipped file.

                    # # --------------Create a folder for extracting zipped file---------------
                    path_of_zipped_file = os.path.join(dir, name_of_file)
                    name_of_folder_for_extraction = name_of_file.removesuffix(".zip") + "__unzipped" # Name of folder that will contain the content of zipped file = name of zipped file (without file extension) + "__unzipped" (to indicate this was a zipped file). This folder will be in the same directory as the found zipped file.

                    while (name_of_folder_for_extraction in subdirs) or (name_of_folder_for_extraction in files):
                        name_of_folder_for_extraction += "__renamed" # Rename folder that will contain the content of zipped file in case of name collision with existing file/folder in the same directory, until it has a unique name.

                    path_to_extract = os.path.join(dir, name_of_folder_for_extraction) # Note: path "dir" does not have "/" at the end. So do not use string concatenation to create this path!
                    # # --------------Create a folder for extracting zipped file---------------

                    # # --------------Attempt to extract zipped file---------------
                    try:
                        with zipfile.ZipFile(path_of_zipped_file, "r") as zip_obj:
                            zip_obj.extractall(path_to_extract) # Extract content of zipped file (only .zip format) to the created folder in directory "dir".
                        os.remove(path_of_zipped_file) # Important: remove zipped file after extracting (so that it will not be found and extracted again).
                    except:
                        pass # Skip if zipped file somehow cannot be extracted.

                    # Note: a try...except... block is used here because sometimes an exception can happen at this point (i.e. not every .zip file can be unzipped by this way).
                    # # --------------Attempt to extract zipped file---------------

            # # --------------Loop through all files in specified directory and search for all zipped files---------------


            # # --------------Loop through all folders in specified directory and search for all zipped folders---------------

            for name_of_subdir in subdirs:
                if name_of_subdir.endswith(".zip"):
                    found_zipped_file_or_folder = True # In case found a zipped folder.

                    # # --------------Create a folder for extracting zipped folder---------------
                    path_of_zipped_folder = os.path.join(dir, name_of_subdir)
                    name_of_folder_for_extraction = name_of_subdir.removesuffix(".zip") + "__unzipped" # Name of folder that will contain the content of zipped folder = name of zipped folder (without extension) + "__unzipped" (to indicate this was a zipped folder). This folder will be in the same directory as the found zipped folder.

                    while (name_of_folder_for_extraction in subdirs) or (name_of_folder_for_extraction in files):
                        name_of_folder_for_extraction += "__renamed" # Rename folder that will contain the content of zipped folder in case of name collision with existing file/folder in the same directory.

                    path_to_extract = os.path.join(dir, name_of_folder_for_extraction)
                    # # --------------Create a folder for extracting zipped folder---------------

                    # # --------------Attempt to extract zipped folder---------------
                    try:
                        with zipfile.ZipFile(path_of_zipped_folder, "r") as zip_obj:
                            zip_obj.extractall(path_to_extract) # Extract content of zipped folder (only .zip format) to the created folder in directory "dir".
                        os.remove(path_of_zipped_folder) # Important: remove zipped folder after extracting (so that it will not be found and extracted again).
                    except:
                        pass # Skip if zipped folder somehow cannot be extracted.

                    # Note: a try...except... block is used here because sometimes an exception can happen at this point (i.e. not every .zip folder can be unzipped by this way).
                    # # --------------Attempt to extract zipped folder---------------

            # # --------------Loop through all folders in specified directory and search for all zipped folders---------------

        if found_zipped_file_or_folder == True:
            continue # In case zipped file(s) and/or folder(s) were found in the given directory with given "path_of_dir", loop/scan through whole directory of given path "path_of_dir" again to search and unzip other files/folders in unzipped file(s) and/or folder(s).
        else:
            break # In case no (more) zipped file or folder found in given directory, end function here.
# # --------------Find and unzip all files/folders in specified directory---------------
