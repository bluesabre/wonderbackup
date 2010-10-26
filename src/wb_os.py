# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wb_os.py
#
# Contains the functions for the operating system dependent tasks.
#
# Modified by Sean Davis on October 26, 2010
# ---------------------------------------------------------------------------- #

from wb_xml import *
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

def get_os_users_location( source ):
    """get_os_users_locations( string source ) -> string

    Returns the location of the profiles, specific per operating system.

    return string location"""
    if source == 'local':
        os = get_os()
        if os[0] == "Windows":
            if os[1] == "Vista" or os[1] == "2008" or os[1] == "7":
                return "C:\\Users\\"
            else:
                return "C:\\Documents and Settings\\"
        elif os[0] == "Linux":
            return "/home/"
        else: # Macs
            return "/Users/"
    else:
        print "External backups are not yet supported."
        return False
		
def get_os_backup_locations( xml_file ):
    """get_os_backup_locations( string username )

    Returns the proper backup locations, specific per OS.

    return list of tuples"""
    xml_doc = xml_file
    xml_locations = get_backup_locations(xml_doc)
    if get_os()[0] == "Windows":
        if get_os()[1] == "Vista" or get_os()[1] == "7" or get_os()[1] == '2008':
            return simple_locations(xml_doc, 'windows', 'vista,2008,7')
        else:
            return simple_locations(xml_doc, 'windows', 'xp,2003')
    elif get_os()[0] == "Linux":
        return simple_locations(xml_doc, 'linux', 'ubuntu')
    else:
        return simple_locations(xml_doc, 'mac', 'osx')
