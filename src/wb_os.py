# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wb_os.py
#
# Contains the functions for the operating system dependent tasks.
#
# Modified by Sean Davis on November 2, 2010
# ---------------------------------------------------------------------------- #

from wb_xml import *
from platform import uname
from os import getenv, listdir, statvfs
from os.path import isdir
from wb_file import byte_to_readable

def detect_os(directory):
    """detect_os( string directory ) -> list

    Returns in list format both the family identifiers and human-readable formats
    of the Operating System detected at the specified directory.

    Return list"""
    folders = listdir(directory)
    for i in range(len(folders)):
        if str(folders[i]).lower() == 'applications':
            return [['mac','osx'],"Mac OS X"]
        elif str(folders[i]).lower() == 'home':
            return [['linux','ubuntu'],"Linux"]
        elif str(folders[i]).lower() == 'windows':
            for j in range(len(folders)):
                if str(folders[j]).lower() == 'documents and settings':
                    return [['windows','xp,2003'],"Windows XP or 2003"]
                elif str(folders[j]).lower() == 'users':
                    return [['windows','vista,2008,7'],"Windows Vista, 2008, or 7"]
    return False

def freespace(directory):
    """
    Returns the number of free bytes on the drive that ``directory`` is on
    """
    space = statvfs(directory)
    size = space.f_bsize * space.f_bavail
    readable = byte_to_readable(size)
    return "Approximately " + readable[0] + " " + readable[1] + " available on this location."

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

def get_users_location( source_dir, os ):
    """get_users_location( string source_dir, list os ) -> string

    Returns the location of the user profiles for the given directory and os.

    return string profiles_dir"""
    if source_dir[len(source_dir)-1] != "/":
        source_dir += "/"
    if os == ['windows','xp,2003']:
        profiles_dir = source_dir + "Documents and Settings/"
    elif os == ['windows','vista,2008,7'] or os == ['mac','osx']:
        profiles_dir = source_dir + "Users/"
    else:
        profiles_dir = source_dir + "home/"
    return profiles_dir


def get_users( source_dir, os ):
    """get_users( string source_dir, list os ) -> list

    Returns a list of the profiles found on the given source_dir and os.

    return list profiles"""
    profiles_dir = get_users_location( source_dir, os )
    structure = listdir(profiles_dir)
    profiles = []
    for i in range(len(structure)):
        if isdir(profiles_dir + structure[i]):
            profiles.append(structure[i])
    return profiles
		
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
