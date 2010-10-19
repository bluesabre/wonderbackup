# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wb_os.py
#
# Contains the functions for the operating system dependent tasks.
#
# Modified by Sean Davis on October 18, 2010
# ---------------------------------------------------------------------------- #

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
            locations = [("Desktop", profile + "Desktop\\"), ("Documents", profile + "Documents\\"), ("Favorites", profile + "Favorites\\"), ("Firefox Profiles", profile + "AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"), ("Music", profile + "Music\\"), ("Pictures", profile + "Pictures\\"), ("Videos", profile + "Videos\\")]
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
