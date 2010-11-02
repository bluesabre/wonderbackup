# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wb_file.py
#
# Contains the functions for the file-related tasks.
#
# Modified by Sean Davis on October 18, 2010
# ---------------------------------------------------------------------------- #

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
