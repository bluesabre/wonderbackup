# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wbBackup.py
#
# Contains the functions used in the backup process.
#
# Modified by Sean Davis on November 11, 2010
# ---------------------------------------------------------------------------- #

from shutil import copy2
from os import walk, listdir, mkdir
from os.path import isdir, isfile, islink
from wbOS import *

def getContents( directory ):
    """getContents( string directory ) -> dict
    
    Returns a dictionary of the contents of the given directory.
    Keys are 'files', 'directories' and 'symlinks'.
    
    Return dict contents"""
    files = []
    directories = []
    symlinks = []
    contents = {}
    for listing in listdir(directory):
        if isdir(directory + listing) and not islink(directory + listing):
            directories.append(listing)
        elif isfile(directory + listing):
            files.append(listing)
        else:
            symlinks.append(listing)
    contents['files'] = files
    contents['directories'] = directories
    contents['symlinks'] = symlinks
    return contents

def excludeFiles(files, exclusionPatterns):
    """excludeFiles( list files, list exclusionPatterns) -> list

    Checks the list 'files' for any files exempted by the list 
    'exclusionPatterns'.  Returns a new list without these files.

    return list files"""
    new = []
    for file in files:
        new.append(file)
    for file in files:
        previousFound = False
        for exclusion in exclusionPatterns:
            if previousFound == False:
                found = True
                if exclusion[0] == '*' and exclusion[1] == '.':
                    for i in range(len(exclusion)-2):
                        if exclusion.lower()[len(exclusion)-i-1] != file.lower()[len(file)-i-1]:
                            found = False
                            break
                else:
                    index = -1
                    for i in range(len(exclusion)):
                        if exclusion[i] == '*':
                            index = i
                            break
                    if index == -1:
                        if exclusion.lower() != file.lower():
                            found = False
                    for j in range(index):
                        if exclusion.lower()[j] != file.lower()[j]:
                            found = False
                if found == True:
                    new.remove(file)
                    previousFound = True
    return new


def copy( originalFile, newFile ):
    """copy( string originalFile, string newFile )

    Copies the file originalFile to the location and file defined by newFile."""
    copy2(originalFile, newFile)

def getBackupFiles( sourceDirectory, exclusionPatterns ):
    """getBackupFiles( string sourceDirectory, list exclusionPatterns ) -> list

    Recursively traverses the directory structure from sourceDirectory and returns
    in an ordered list, the absolute locations for each file that does not match
    any of the exclusionPatterns.

    Return list absoluteFiles"""
    sourceDirectory = dirString(source_directory)
    contents = getContents(sourceDirectory)
    files = excludeFiles(contents['files'], exclusionPatterns)
    absoluteFiles = []
    for i in range(len(files)):
        absoluteFiles.append( sourceDirectory + files[i] )
    directories = contents['directories']
    for directory in directories:
        absoluteFiles += getBackupFiles(sourceDirectory + directory, exclusionPatterns) 
    absoluteFiles.sort()
    return absoluteFiles

def makeBackupFolders( sourceDirectory, targetDirectory ):
    """makeBackupFolders( string sourceDirectory, string targetDirectory )

    Recreates the folder structure of sourceDirectory in targetDirectory.

    Return True"""
    sourceDirectory = dirString(sourceDirectory)
    targetDirectory = dirString(targetDirectory)
    contents = getContents(sourceDirectory)
    directories = contents['directories']
    for directory in directories:
        mkdir(targetDirectory + directory)
        makeBackupFolders( sourceDirectory + directory, targetDirectory + directory )
    return True

def targetFilenames( sourceDirectory, targetDirectory, files ):
    """targetFilenames( string sourceDirectory, string targetDirectory, list files ) ->: list

    Returns a list of the absolute locations for the newly created files.

    Return list newfiles"""
    sourceDirectory = dirString(sourceDirectory)
    targetDirectory = dirString(targetDirectory)
    newfiles = []
    for i in files:
        newfiles.append( i.replace(sourceDirectory,targetDirectory) )
    return newfiles
