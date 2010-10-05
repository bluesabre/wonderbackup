# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# all_functions.py
#
# Modified by Sean Davis on October 5, 2010
# ---------------------------------------------------------------------------- #

# File Functions
import os
import datetime

def get_extension_index( filename ):
    """get_extension_index( string filename ) -> integer
    
    Returns the index of the period after which the filetype extension is found.
    
    return int index"""
    for i in range(len(filename)):
        if filename[i] == ".":
            index = i
    return index

def get_extension( filename ):
    """get_extension( string filename ) -> string
    
    Returns the extension of the filename in lowercase.
    
    return string extension"""
    l_filename = len(filename)
    index = get_extension_index(filename)
    extension = ""
    for i in range(index+1, l_filename):
        extension += filename[i]
    return extension.lower()

def byte_to_readable( n_bytes ):
    """byte_to_readable( long int n_bytes ) -> tuple
    
    Returns a tuple containing the number of bytes in its highest representation and its measurement.
    
    return ( string n_units, string measurement )"""
    readable = ""
    if n_bytes >= 1073741824:
        return (str(n_bytes/1073741824), "GB")
    elif n_bytes >= 1048576:
        return (str(n_bytes/1048576), "MB")
    elif n_bytes >= 1024:
        return (str(n_bytes/1024), "kB")
    else:
        return (str(n_bytes), " B")

def get_attributes( file, filename ):
    """get_attributes( string file, string filename ) -> tuple
    
    Returns a tuple containing the filename, its size, and modification date.
    
    return ( string filename, ( string n_units, string measurement ), ( month, day, year ) )"""
    size = os.stat(file).st_size
    date = str(datetime.datetime.fromtimestamp(os.path.getmtime(file)).date())
    year = date[2] + date[3]
    month = date[5] + date[6]
    day = date[8] + date[9]
    return (filename, byte_to_readable(size), (month, day, year))




# Output Functions
def truncate_directory( directory, size ):
    """truncate_directory( string directory, int size )

    Returns a string directory truncated to the given length size.

    return string directory"""
    if len(directory) > size-2:
        truncated = ""
        for i in range(len(directory)-size-2, len(directory)):
            truncated += directory[0]
    else:
        return directory

def terminal_filename( filename, fit_size ):
    """terminal_filename( string filename, int fit_size) -> string
    
    Returns a string of the filename designed to fit in the given amount of space.
    
    return string filename"""
    if len(filename) >= fit_size:
        extension = get_extension(filename)
        truncated = ""
        for i in range(fit_size-3-len(extension)):
            truncated += filename[i]
        truncated += "..."
        truncated += extension
        return truncated
    else:
        extended = ""
        for i in range(len(filename)):
            extended += filename[i]
        for i in range(fit_size - len(filename)):
            extended += " "
        return extended
        
def terminal_size( size, measurement ):
    """terminal_size( string size, string measurement ) -> string
    
    Returns a string of the file size in a format that fits six blocks.
    
    return string file_size"""
    if len(size) == 4:
        return size + measurement
    elif len(size) == 3:
        return "~" + size + measurement
    elif len(size) == 2:
        return "~" + size + " " + measurement
    else:
        return "~ " + size + " " + measurement
    
def terminal_modified( date ):
    """terminal_modified( string date ) -> string
    
    Returns a string of the modified date in the following format: MM/DD/YY
    
    return string modification_date"""
    return str(date[0]) + "/" + str(date[1]) + "/" + str(date[2])

def terminal_output( directory, files, size=79 ): #Size must be greater than 32.
    """terminal_output( string directory, list files, int size )
    
    Prints the files given in a format that is easy on the eyes and easy to follow."""
    if directory[len(directory)-1] != "/":
        directory += "/"
    title_size = truncate_directory(directory, size)
    title_upper = "o-"
    for i in range(len(title_size)):
        title_upper += "-"
    title_upper += "-o"
    print title_upper
    print "| " + title_size + " |"
    line = "o-"
    for i in range(size-24):
        line += "-"
    line += "-o--------o----------o"
    print line
    infoline = "| Filename"
    for i in range(size-32):
        infoline += " "
    infoline += " |  Size  | Modified |"
    print infoline
    print line
    for file in files:
        attrib = get_attributes( directory + str(file), str(file) )
        print "| " + terminal_filename(attrib[0], size-24) + " | "  + terminal_size(attrib[1][0], attrib[1][1]) + " | " + terminal_modified(attrib[2]) + " |"
    print line



# Backup Functions
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
    terminal_output(origin_directory, files)
    directories = contents[1]
    if contents[2] > 0:
        print "There are " + str(contents[2]) + " symbolic links in this directory!"
    for file in files:
        copy( origin_directory + file, target_directory + file )
    for directory in directories:
        mkdir(target_directory + directory)
        copy_multiple(origin_directory + directory, target_directory + directory, excluded_filetypes)
    return True




# OS Specific Functions
from platform import uname
from os import getenv
from os.path import isdir

def get_os():
    """Returns the Operating System family and version.

    return [os_family, os_version]"""
    return [uname()[0], uname()[2]]

def get_logged_in():
    """Returns the currently logged in user.

    return string username"""
    if get_os()[0] == "Windows":
        return getenv("USERNAME")
    else:
        return getenv("USER")

def check_valid_location( location ):
    """check_valid_location( string location )

    Checks if a given location actually exists.

    return bool"""
    if isdir(location):
        return True
		
def get_user_locations( username ):
    """get_user_locations( string username )

    Returns the proper backup locations, specific per OS.

    return list of tuples"""
    if get_os()[0] == "Windows":
        if get_os()[1] == "Vista" or get_os()[1] == "7":
            profile = "C:\\Users\\" + username + "\\"
            locations = [("Desktop", profile + "Documents\\"), ("Documents", profile + "Documents\\"), ("Favorites", profile + "Favorites\\"), ("Firefox Profiles", profile + "AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"), ("Music", profile + "Music\\"), ("Pictures", profile + "Pictures\\"), ("Videos", profile + "Videos\\")]
        else:
            profile = "C:\\Documents and Settings\\" + username + "\\"
            locations = [("Desktop", profile + "Desktop\\"), ("Favorites", profile + "Favorites"), ("Firefox Profiles", profile + "Application Data\\Mozilla\\Firefox\\Profiles\\"), ("My Documents", profile + "My Documents\\")]
    elif get_os()[0] == "Linux":
        profile = "/home/" + username + "/"
        locations = [("Desktop", profile + "Desktop/"), ("Documents", profile + "Documents/"), ("Music", profile + "Music/"), ("Mozilla (Firefox and Thunderbird) Profiles", profile + ".mozilla/"), ("Pictures", profile + "Pictures/"), ("Videos", profile + "Videos/")]
    else:
        profile = "/Users/" + username + "/"
        locations = [("Desktop", profile + "Desktop/"), ("Documents", profile + "Documents/"), ("Movies", profile + "Movies/"), ("Music", profile + "Music/"), ("Pictures", profile + "Pictures/")]
    all_locations = []
    for each in locations:
        if isdir(each[1]):
            all_locations.append(each)
    return all_locations
