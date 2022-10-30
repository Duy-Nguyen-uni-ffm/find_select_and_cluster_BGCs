''' This module has one function that creates an empty directory with a given path if the path does not exist yet, otherwise returns the given path. '''


import os  # Necessary!


def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path # Create directory with given path (if not existed) and return this path
