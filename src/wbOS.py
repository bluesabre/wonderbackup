# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wbOS.py
#
# Contains the functions for the operating system dependent tasks.
#
# Modified by Sean Davis on November 14, 2010
# ---------------------------------------------------------------------------- #

from os import getenv, listdir
from os.path import isdir
from platform import uname

from wbFile import readableSize
from wbXML import *


try:
    from os import statvfs
except ImportError:
    pass

def dirString( directory ):
    """dirString( string directory ) -> string
    
    Returns the directory listing in the proper format based on the host
    operating system, and if the listing is not a file, adds trailing slashes.
    
    return string dir"""
    if detectOS()['family'] == 'windows':
        dir = directory.replace('/','\\')
        if isdir(dir) and dir[len(dir)-1] != '\\':
            return dir + '\\'
        else:
            return dir
    else:
        dir = directory.replace('\\','/')
        if isdir(dir) and dir[len(dir)-1] != '/':
            return dir + '/'
        else:
            return dir

def detectOS( directory='local' ):
    """detectOS( string directory ) -> dict

    Returns a dictionary of the detected Operating System.  This function works 
    with both local and external directories, and can be called with the directory 
    or left blank to assume local.
    
    Keys are 'family', 'version' and 'readable'.

    Return dict """
    if directory == 'local':
        osFamily = uname()[0].lower()
        osVersion = uname()[2].lower()
        if osFamily == 'windows':
            if osVersion == "vista" or osVersion == "2008" or osVersion == "7":
                return {'family':'windows', 'version':'vista,2008,7', 'readable':'Windows Vista, 2008, or 7'}
            else:
                return {'family':'windows', 'version':'xp,2003', 'readable':'Windows XP or 2003'}
        elif osFamily == 'linux':
            return {'family':'linux', 'version':'ubuntu', 'readable':'Linux'}
        else: # osFamily == 'mac'
            return {'family':'mac', 'version':'osx', 'readable':'Mac OS X'}
    else:
        folders = listdir( dirString(directory) )
        for i in range(len(folders)):
            if str(folders[i]).lower() == 'applications':
                return {'family':'mac', 'version':'osx', 'readable':'Mac OS X'}
            elif str(folders[i]).lower() == 'home':
                return {'family':'linux', 'version':'ubuntu', 'readable':'Linux'}
            elif str(folders[i]).lower() == 'windows':
                for j in range(len(folders)):
                    if str(folders[j]).lower() == 'users':
                        return {'family':'windows', 'version':'vista,2008,7', 'readable':'Windows Vista, 2008, or 7'}
                return {'family':'windows', 'version':'xp,2003', 'readable':'Windows XP or 2003'}
    return False
    


def freespace(directory):
    """freespace( string directory ) -> string
    
    Returns the amount of free space available for the given directory in its
    highest representation.
    
    return string"""
    if detectOS()['family'] == 'linux':
        space = statvfs(directory)
        size = space.f_bsize * space.f_bavail
        readable = readableSize(size)
        if str(readable) != "0":
            return "Approximately " + readable + " available on this location."
    else:
        return ""

def getCurrentUser():
    """Returns the currently logged in user.

    return string username"""
    if detectOS()['family'] == "windows":
        return getenv("USERNAME")
    else:
        return getenv("USER")

def checkLocation( directory ):
    """checkLocation( string directory )

    Checks if a given location actually exists.

    return bool"""
    if isdir( dirString(directory) ):
        return True
    else:
        return False

def getProfilesFolder( sourceDirectory ):
    """getProfilesFolder( string sourceDirectory ) -> string

    Returns the location of the user profiles for the given sourceDirectory.

    return string profilesDir"""
    operatingSystem = detectOS( sourceDirectory )
    if operatingSystem['family'] == 'windows' and operatingSystem['version'] == 'xp,2003':
        profilesDir = sourceDirectory + "Documents and Settings/"
    if operatingSystem['family'] == 'windows' and operatingSystem['version'] == 'vista,2008,7':
        profilesDir = sourceDirectory + "Users/"
    if operatingSystem['family'] == 'mac':
        profilesDir = sourceDirectory + "Users/"
    if operatingSystem['family'] == 'linux':
        profilesDir = sourceDirectory + "home/"
    return dirString( profilesDir )

def getProfiles( sourceDirectory ):
    """getProfiles( string sourceDirectory ) -> list

    Returns a list of the profiles found on the given sourceDirectory.

    return list profiles"""
    profiles_dir = getProfilesFolder( dirString(sourceDirectory) )
    structure = listdir( dirString(profiles_dir) )
    profiles = []
    for i in range(len(structure)):
        if checkLocation( dirString(profiles_dir + structure[i]) ):
            profiles.append(structure[i])
    return profiles
