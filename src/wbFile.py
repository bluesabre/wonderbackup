# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wbFile.py
#
# Contains the functions for the file-related tasks.
#
# Modified by Sean Davis on December 7, 2010
# ---------------------------------------------------------------------------- #

import os
import datetime


def readableSize( n_bytes ):
    """Return a string containing the size 'n_bytes' in its highest
    representation to the second decimal place.
    
    Keyword arguments:
    n_bytes -- a long int value representing filesize in bytes.
    
    """
    readable = ""
    if n_bytes >= 1073741824:
        value = (str(n_bytes/1073741824.0), "GB")
    elif n_bytes >= 1048576:
        value = (str(n_bytes/1048576.0), "MB")
    elif n_bytes >= 1024:
        value = (str(n_bytes/1024.0), "kB")
    else:
        value = (str(n_bytes), "B")
    size = ""
    for i in range(len(value[0])):
        if value[0][i] == ".":
            if len(value[0])-i < 3:
                for j in range(len(value[0])-i):
                    size += value[0][i+j]
            else:
                for j in range(3):
                    size += value[0][i+j]
            return size + " " + value[1]
        else:
            size += value[0][i]
    return value[0] + " " + value[1]


def getAttributes( filename ):
    """Return a dictionary containing the file size and modification time.
    
    Keyword arguments:
    filename -- a string containing the path to a file.
    
    Dictionary keys:
    size -- a string containing the file size in its highest representation to
    the second decimal point.
    modified -- a dictionary containing the file modification time.  Keys are
    'year', 'month', 'day', and 'time'.
    
    """
    attributes = {}
    attributes['size'] = readableSize(os.stat(filename).st_size)
    mod_date = {}
    date = str(datetime.datetime.fromtimestamp(os.path.getmtime(filename)).date())
    mod_date['year'] = date[0] + date[1] + date[2] + date[3]
    mod_date['month'] = date[5] + date[6]
    mod_date['day'] = date[8] + date[9]
    mod_date['time'] = date = str(datetime.datetime.fromtimestamp(os.path.getmtime(filename)).time())
    attributes['modified'] = mod_date
    
    return attributes