# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wb_backup.py
#
# Contains the functions used in the backup process.
#
# Modified by Sean Davis on October 26, 2010
# ---------------------------------------------------------------------------- #

from shutil import copy2
from os import walk, listdir, mkdir
from os.path import isdir, isfile, islink

def get_contents(directory):
    """get_contents( string directory ) -> tuple

    Gathers the contents of the string 'directory' and returns a tuple
    in the following format:
    
    return ( list files , list directories, int symlinks )"""
    files = []
    directories = []
    symlinks = 0
    for listing in listdir(directory):
        if isdir(directory + listing) and not islink(directory + listing):
            directories.append(listing)
        elif isfile(directory + listing):
            files.append(listing)
        else:
            symlinks += 1
    return (files, directories, symlinks)

def remove_excluded(files, excluded_filetypes):
    """remove_excluded( list files, list excluded_filetypes) -> list

    Checks the list 'files' for any extensions exempted by the list 
    'excluded_filetypes'.  Returns a new list without these files.

    return ( list files )"""
    new = []
    for file in files:
        new.append(file)
    for each in files:
        l_file = len(each)
        for filetype in excluded_filetypes:
            found = True
            l_filetype = len(filetype)
            if l_filetype <= l_file:
                for i in range(l_filetype):
                    if each[l_file-l_filetype+i].lower() != filetype[i].lower(): # Not case-sensitive
                        found = False
                        break
            if found == True:
                new.remove(each)
                break
    return new

def copy( original_file, new_location ):
    """copy( string original_file, string new_location )

    Copies the given original_file to the new_location."""
    copy2(original_file, new_location)

def copy_multiple(origin_directory, target_directory, excluded_filetypes):
    """copy_multiple( string origin_directory, string target_directory, list excluded_filetypes)

    Recursively copies multiple files from origin_directory to target_directory,
    ignoring any files of the excluded_filetypes.

    Return True"""
    if origin_directory[len(origin_directory)-1] != '/':
        origin_directory += '/'
    if target_directory[len(target_directory)-1] != '/':
        target_directory += '/'
    contents = get_contents(origin_directory)
    files = remove_excluded(contents[0], excluded_filetypes)
#    terminal_output(origin_directory, files)
    directories = contents[1]
    if contents[2] > 0:
        print "There are " + str(contents[2]) + " symbolic links in this directory!"
    for file in files:
        copy( origin_directory + file, target_directory + file )
    for directory in directories:
        mkdir(target_directory + directory)
        copy_multiple(origin_directory + directory, target_directory + directory, excluded_filetypes)
    return True
