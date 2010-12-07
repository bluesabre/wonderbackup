# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wbBackup.py
#
# Contains the functions used in the backup process.
#
# Modified by Sean Davis on December 7, 2010
# ---------------------------------------------------------------------------- #

from os import walk, listdir, mkdir, stat
from os.path import isdir, isfile, islink
from shutil import copy2
from time import strftime

from wbOS import *


def timestamp():
    """Return a string containing the current time and date in the format:
      YYYY-MM-DD-HH:MM:SS
    """
    return strftime("%Y-%m-%d-%H:%M:%S")

def getContents(directory):
    """Returns a dictionary containing the contents of 'directory'.
    
    Keyword arguments:
    directory -- a string containing a valid path.
    
    Dictionary keys:
    files -- a list of files.
    directories -- a list of subdirectories.
    symlinks -- a list of symbolic links (not including Windows symbolic links.)
    
    """
    files = []
    directories = []
    symlinks = []
    contents = {}
    try:
        allListings = listdir(directory)
        for listing in listdir(directory):
            if isdir(directory + listing) and not islink(directory + listing):
                directories.append(listing)
            elif isfile(directory + listing):
                files.append(listing)
            else:
                symlinks.append(listing)
    except Exception: # Windows symbolic links are not valid paths.
        pass
    contents['files'] = files
    contents['directories'] = directories
    contents['symlinks'] = symlinks
    return contents

def excludeFiles(files, exclusionPatterns):
    """Return a list of files that do not match any exclusion patterns.
    
    Keyword arguments:
    files -- a list of files.
    exclusionPatterns -- a list of exclusion patterns.
    
    """
    new = []
    for file in files:
        new.append(file)
    for file in files:
        previousFound = False
        for exclusion in exclusionPatterns:
            if previousFound == False:
                found = True
                if exclusion[0] == '*' and exclusion[1] == '.':
                    for i in range(len(exclusion) - 2):
                        if exclusion.lower()[len(exclusion) - i - 1] != \
                                             file.lower()[len(file) - i - 1]:
                            found = False
                            break
                else:
                    if exclusion == "~$*":
                        found = False
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
                            print j
                            if exclusion.lower()[j] != file.lower()[j]:
                                found = False
                if found == True:
                    new.remove(file)
                    previousFound = True
    return new

def copy(originalFile, newFile):
    """Copy a file from one location to another.
    
    Keyword arguments:
    originalFile -- a string containing the path to the original file location.
    newFile -- a string containing the path the the new file location.
    
    Return:
    True, if no errors are encountered.
    String, containing the error if encountered.
    
    """
    try: # Attempts to copy the file.
        copy2(originalFile, newFile)
    except Exception: # If the copy fails, an error is returned.
        if not isfile(newFile) or stat(originalFile).st_size != \
                                  stat(newFile).st_size:
            return timestamp() + " FILE_COPY_ERROR: " + originalFile
    return True
            

def getBackupFiles(sourceDirectory, exclusionPatterns):
    """Return a list of files to be backed up, without those that are excluded.
    
    Keyword arguments:
    sourceDirectory -- a string containing the path to the source directory.
    exclusionPatterns -- a list of exclusion patterns.
    
    """
    sourceDirectory = dirString(sourceDirectory)
    contents = getContents(sourceDirectory)
    files = excludeFiles(contents['files'], exclusionPatterns)
    absoluteFiles = []
    for i in range(len(files)):
        absoluteFiles.append(sourceDirectory + files[i])
    directories = contents['directories']
    for directory in directories:
        absoluteFiles += getBackupFiles(sourceDirectory + directory, 
                                        exclusionPatterns) 
    absoluteFiles.sort()
    return absoluteFiles

def makeBackupFolders(sourceDirectory, targetDirectory):
    """Recreate the folder structure of the source directory in the target
    directory.  Return a list of any errors encountered.
    
    Keyword arguments:
    sourceDirectory -- a string containing the path to the source directory.
    targetDirectory -- a string containing the path to the target directory.
    
    """
    errors = []
    sourceDirectory = dirString(sourceDirectory)
    targetDirectory = dirString(targetDirectory)
    contents = getContents(sourceDirectory)
    directories = contents['directories']
    for directory in directories:
        try:
            if not checkLocation(targetDirectory + directory):
                mkdir(targetDirectory + directory)
            makeBackupFolders(sourceDirectory + directory, 
                              targetDirectory + directory)
        except Exception:
            errors.append(timestamp() + " DIRECTORY_ACCESS_ERROR: " + \
                          sourceDirectory)
    return errors

def targetFilenames(sourceDirectory, targetDirectory, files):
    """Return a list of absolute locations for the newly created files.
    
    Keyword arguments:
    sourceDirectory -- a string containing the path to the source directory.
    targetDirectory -- a string containing the path to the target directory.
    files -- a list of the absolute locations of files to be backed up from the
             source directory.    
    
    """
    sourceDirectory = dirString(sourceDirectory)
    targetDirectory = dirString(targetDirectory)
    newfiles = []
    for i in files:
        newfiles.append(i.replace(sourceDirectory,targetDirectory))
    return newfiles