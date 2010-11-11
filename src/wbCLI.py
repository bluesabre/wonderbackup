# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wbCLI.py
#
# Contains the functions for the command-line interface.
#
# Modified by Sean Davis on November 11, 2010
# ---------------------------------------------------------------------------- #

from wbBackup import *
from wbFile import *
from wbOS import *
from wbXML import *

# Needs to include messages and we need updated messages for this part of the
# process.
def cliBackup( messages, backupLocations, targetDirectory, exclusionPatterns ):
    """cliBackup( dict message, list backupLocations, string targetDirectory, list exclusionPatterns)
    
    Performs the command-line backup, using the language from messages, of files
    from the list backupLocations to the targetDirectory, excluding any files
    that match the exclusionPatterns."""

    for key in backupLocations.keys():
        print messages['backup-progress']['category-backup'] + "[" + key + "]\n\n"
        mkdir(dirString(targetDirectory) + key)
        print "\t" + messages['backup-progress']['getting-files'] + backupLocations[key] + "..."
        backupFiles = getBackupFiles( backupLocations[key], exclusionPatterns )
        backupFiles.sort()
        print "\t" + messages['backup-progress']['found'] + str(len(backupFiles)-1) + messages['backup-progress']['files-to-backup']
    
        print "\t" + messages['backup-progress']['building-structure'] + targetDirectory + "...\n\n"
        makeBackupFolders( backupLocations[key], dirString(targetDirectory) + key )
        
        print "\t" + messages['backup-progress']['configuring-target'] + "\n\n"
        targetFiles = targetFilenames( backupLocations[key], dirString( dirString(targetDirectory) + key), backupFiles )
        targetFiles.sort()
        
        total = len(backupFiles)-1
        for i in range(len(backupFiles)):
            print messages['backup-progress']['copying-file'] + str(i) + messages['backup-progress']['of'] + str(total) + "..."
            copy( backupFiles[i], targetFiles[i] )        

def selectBackupType( messages ):
    """selectBackupType( dict messages ) -> string

    The first of the commandline backup steps.

    Runs the user through the backup type selection, returning the selection as 
    a string, 'local', 'external', or 'preconfigured'.

    return string answer"""
    print messages['backup']['backup-type']
    answer = 0
    while answer < 1 or answer > 3:
        answer = input("1. " + messages['backup-option']['local'] + "\n2. " + messages['backup-option']['external'] + "\n3. " + messages['backup-option']['preconfigured'] + "\n\n" + messages['prompt']['enter-selection'])
    print "\n\n\n"
    if answer == 1:
        return 'local'
    elif answer == 2:
        return 'external'

def selectSource(messages, backupType):
    """select_source( dict messages, string backupType ) -> string

    The second of the commandline backup steps.

    Runs the user through the backup source selection, if necessary, returning 
    the location as a string.

    return string location"""
    if backupType == 'local':
        if detectOS()['family'] == 'windows':
            return 'C:\\'
        else:
            return '/'
    else:
        print messages['backup']['select-source']
        print "\n\n\n"

def selectTarget( messages ):
    """selectTarget( dict messages ) -> string
    
    The third of the commandline backup steps.

    Returns the location that is entered by the user.  Checks for validity and 
    adds necessary trailing slashes.

    return string location"""
    print messages['backup']['backup-type']
    location = "a"
    while not checkLocation(location):
        location = raw_input(messages['prompt']['enter-location'] + "\n ")
    print "\n\n\n"
    return location

def selectUser( messages, source ):
    """selectUser( dict messages, string source ) -> string
    
    The fourth of the commandline backup steps.

    Returns the user profile selected for backup.

    return string profile"""
    print messages['backup']['select-user']
    users = getProfiles( source )
    for i in range(1,len(users)+1):
        print str(i) + ". " + users[i-1]
    ans = 0
    while ans < 1 or ans > len(users):
        ans = input(messages['prompt']['select-profile'])
    print "\n\n\n"
    return users[ans-1]
   
def selectBackupLocations( messages, source, user, locations ):
    """selectBackupLocations( dict messages, string source, string user, dict locations ) -> dict
    
    The fifth of the commandline backup steps.

    Returns the list of backup locations to be backed up.

    return dict selectedLocations"""
    selectedLocations = {}
    operatingSystem = detectOS(source)
    profileFolder = dirString( getProfilesFolder( source ) + user )
    print messages['backup']['select-locations']
    for location in locations.keys():
        ans = ""
        while ans != 'y' and ans != 'n':
            ans = raw_input(messages['prompt']['to-backup'] + location + "?\ny or n: ")
            ans = ans.lower()
        if ans == 'y':
            selectedLocations[location] = dirString( profileFolder + locations[location] )
    print "\n\n\n"
    return selectedLocations    
    
def selectExclusions( messages, exclusions ):
    """selectExclusions( dict messages, dict exclusions ) -> list
    
    The sixth of the commandline backup steps.

    Returns a list of the exclusion patterns, as selected by the user.

    return list exclusions"""
    print messages['backup']['select-exclusions']
    exclusionPatterns = []
    for pattern in exclusions.keys():
        ans = ""
        while ans != 'y' and ans != 'n':
            ans = raw_input(messages['prompt']['to-exclude'] + pattern + "?\ny or n: ")
            ans = ans.lower()
        if ans == 'y':
            for exclusion in exclusions[pattern]:
                exclusionPatterns.append(exclusion)
    exclusionPatterns.sort()
    print "\n\n\n"
    return exclusionPatterns

def startBackup( messages, backupType, sourceDirectory, targetDirectory, user, backupLocations, exclusions ):
    """startBackup( dict messages, string backupType, string sourceDirectory, string targetDirectory, string user, dict backupLocations, list exclusions )

    Confirms that all settings are correct and begins the backup program."""
    print messages['summary']['proceed']
    print messages['summary']['details']
    print messages['summary']['type'] + str(backupType)
    print messages['summary']['source'] + str(sourceDirectory)
    print messages['summary']['target'] + str(targetDirectory)
    print messages['summary']['profile'] + str(user)
    print messages['summary']['locations'] + "\n"
    for location in backupLocations.keys():
        print location + " at [" + backupLocations[location] + "]"
    print messages['summary']['exclusions'] + "\n " + str(exclusions)
    raw_input(messages['backup']['proceed'])
    
    cliBackup( messages, backupLocations, targetDirectory, exclusions )

#----------------------------------------------------------------------
if __name__ == "__main__":
    language = 'en'
    settings = readXML("wonderbackup.xml")
    messages = getMessages(readXML("localizations.xml"), language)
# Messages are in the format (backup_wizard, backup_options, dialogs, prompts, summary, welcome)
    exclusions = getExclusions(settings)

# Welcome Message
    print messages['welcome']['welcome'] #Welcome Message
# Backup Type
    backupType = selectBackupType(messages) 
# Select Source
    sourceDirectory = selectSource(messages, backupType)
    locations = getLocations(settings, detectOS(sourceDirectory)['family'], detectOS(sourceDirectory)['version'])
# Select Target
    targetDirectory = selectTarget( messages )
# Select User
    user = selectUser( messages, sourceDirectory )
# Select Backup Locations
    backupLocations = selectBackupLocations( messages, sourceDirectory, user, locations )
# Select Exclusions
    selectedExclusions = selectExclusions( messages, exclusions )
# Start the Backup Progress
    startBackup( messages, backupType, sourceDirectory, targetDirectory, user, backupLocations, selectedExclusions )
