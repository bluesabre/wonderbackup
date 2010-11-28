# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wbCLI.py
#
# Contains the functions for the command-line interface.
#
# Modified by Sean Davis on November 27, 2010
# ---------------------------------------------------------------------------- #

from wbBackup import *
from wbFile import *
from wbOS import *
from wbXML import *


def selectBackupType(messages):
    """The first step of the commandline backup wizard.
    Prompt the user for the type of backup to be performed.  
    Return a string containing the type of backup selected.
    
    Keyword arguments:
    messages -- the dictionary of all output for the locale.
    
    """
    print messages['backup']['backup-type']
    answer = 0
    while answer < 1 or answer > 3:
        print "1. " + messages['backup-option']['local'] + "\n" + \
              "2. " + messages['backup-option']['external'] + "\n" + \
              "3. " + messages['backup-option']['preconfigured'] + "\n\n"
        try:
            answer = input(messages['prompt']['enter-selection'])
        except Exception:
            print messages['error']['enter-integer-123'] + "\n"
    print "\n\n\n"
    if answer == 1:
        return 'local'
    elif answer == 2:
        return 'external'

def selectSource(messages, backupType):
    """The second step of the commandline backup wizard.
    Prompt the user (if necessary) of the source device to backup.
    Return a string containing the source that is either entered by the user or
    automatically generated.
    
    Keyword arguments:
    messages -- the dictionary of all output for the locale.
    
    """
    if backupType == 'local':
        if detectOS()['family'] == 'windows':
            return 'C:\\'
        else:
            return '/'
    else:
        print messages['backup']['select-source']
        location = "a"
        while not checkLocation(location):
            location = raw_input(messages['prompt']['enter-location'] + "\n ")
            if location == '/': location = "\\"
        if location == "\\": location = '/'
        print "\n\n\n"
        return location

def selectTarget(messages):
    """The third step of the commandline backup wizard.
    Prompt the user for the target location to store the backup.
    Return a string containing the location entered by the user.
    
    Keyword arguments:
    messages -- the dictionary of all output for the locale.
    
    """
    print messages['backup']['select-target']
    location = "a"
    while not checkLocation(location):
        location = raw_input(messages['prompt']['enter-location'] + "\n ")
    print "\n\n\n"
    return location

def selectUser(messages, source):
    """The fourth step of the commandline backup wizard.
    Prompt the user for the profile to be backed up.
    Return a string containing the user profile name selected by the user.
    
    Keyword arguments:
    messages -- the dictionary of all output for the locale.
    source -- a string containing the path to the source device.
    
    """
    print messages['backup']['select-user']
    users = getProfiles(source)
    for i in range(1, len(users) + 1):
        print str(i) + ". " + users[i - 1]
    ans = 0
    while ans < 1 or ans > len(users):
        try:
            ans = input(messages['prompt']['select-profile'])
        except Exception:
            print "\n" + messages['error']['enter-integer-1to'] + \
                  str(len(users)) + "\n"
    print "\n\n\n"
    return users[ans - 1]
   
def selectBackupLocations(messages, source, user, locations):
    """The fifth step of the commandline backup wizard.
    Prompt the user for the profile locations to be backed up.
    Return a dictionary of the profile locations selected by the user.
    
    Keyword arguments:
    messages -- the dictionary of all output for the locale.
    source -- a string containing the path to the source device.
    user -- a string containing a user profile name.
    locations -- a dictionary of all locations for every Operating System.
    
    """
    selectedLocations = {}
    operatingSystem = detectOS(source)
    profileFolder = dirString( getProfilesFolder(source) + user )
    print messages['backup']['select-locations']
    for location in locations.keys():
        ans = ""
        while ans != 'y' and ans != 'n':
            ans = raw_input(messages['prompt']['to-backup'] + location + \
                            "?\ny or n: ")
            ans = ans.lower()
        if ans == 'y':
            selectedLocations[location] = dirString(profileFolder + \
                                                    locations[location])
    print "\n\n\n"
    return selectedLocations    
    
def selectExclusions(messages, exclusions):
    """The sixth step of the commandline backup wizard.
    Prompt the user for any exclusions to be made for the files backed up.
    Return a list of exclusion patterns.
    
    Keyword arguments:
    messages -- the dictionary of all output for the locale.
    exclusions -- a dictionary of all possibile exclusion options.
    
    """
    print messages['backup']['select-exclusions']
    exclusionPatterns = []
    for pattern in exclusions.keys():
        ans = ""
        while ans != 'y' and ans != 'n':
            ans = raw_input(messages['prompt']['to-exclude'] + pattern + \
                            "?\ny or n: ")
            ans = ans.lower()
        if ans == 'y':
            for exclusion in exclusions[pattern]:
                exclusionPatterns.append(exclusion)
    exclusionPatterns.sort()
    print "\n\n\n"
    return exclusionPatterns
    
def cliBackup(messages, backupLocations, targetDirectory, exclusionPatterns):
    """The seventh and final step of the commandline backup wizard.
    Begin the backup process, following user confirmation.
    
    Keyword arguments:
    messages -- the dictionary of all output for the locale.
    backupLocations -- a dictionary of locations selected to backup.
    targetDirectory -- a string containing the location to store the backup.
    exclusionPatterns -- a list of exclusion patterns.
    
    """
    try:
        ErrorLog = open(dirString(targetDirectory) + "ErrorLog.txt", 'a')
    except Exception:
        print messages['error']['not-writable'] + "\n"
        print messages['error']['exit'] + "\n"
        exit()
    ErrorLog.write("[Wonder Backup Session " + timestamp() + "]\r\n")
    for key in backupLocations.keys():
        print messages['backup-progress']['category-backup'] + "[" + key + "]\n"
        try:
            mkdir(dirString(targetDirectory) + key)
        except Exception:
            print messages['error']['directory-exists'] + "\n"
        print "\t" + messages['backup-progress']['getting-files'] + \
              backupLocations[key] + "..."
        backupFiles = getBackupFiles(backupLocations[key], exclusionPatterns)
        backupFiles.sort()
        print "\t" + messages['backup-progress']['found'] + \
              str(len(backupFiles) - 1) + \
              messages['backup-progress']['files-to-backup']
    
        print "\t" + messages['backup-progress']['building-structure'] + \
              targetDirectory + "...\n\n"
        makeBackupFolders(backupLocations[key], dirString(targetDirectory) + \
                          key)
        
        print "\t" + messages['backup-progress']['configuring-target'] + "\n\n"
        targetFiles = targetFilenames(backupLocations[key], 
                                      dirString(dirString(targetDirectory) + \
                                                key), backupFiles )
        targetFiles.sort()
        
        total = len(backupFiles) - 1
        for i in range(len(backupFiles)):
            print messages['backup-progress']['copying-file'] + str(i) + \
                  messages['backup-progress']['of'] + str(total) + "..."
            if isfile(targetFiles[i]):
                if getAttributes(backupFiles[i]) != getAttributes(targetFiles[i]):
                    print "  Updating [" + targetFiles[i] + "]\r\n"
                    CopyError = copy(backupFiles[i], targetFiles[i])
                    if CopyError != True:
                        ErrorLog.write(CopyError + "\r\n")   
                else:
                    print "  [" + targetFiles[i] + "] already up-to-date.\r\n" 
            else:
                print "  Copying [" + targetFiles[i] + "]\r\n"
                CopyError = copy( backupFiles[i], targetFiles[i] )
                if CopyError != True:
                    ErrorLog.write(CopyError + "\r\n")
    ErrorLog.write("[END SESSION]\r\n\r\n\r\n\r\n")
    ErrorLog.close()
    
def startBackup(messages, backupType, sourceDirectory, targetDirectory, user, 
                backupLocations, exclusions ):
    """Request confirmation that the selected backup settings are correct.
    Start the backup when the user has confirmed the settings.
    
    Keyword arguments:
    messages -- the dictionary of all output for the locale.
    backupType -- a string containing the backup type.
    sourceDirectory -- a string containing the path to the source device.
    targetDirectort -- a string containing the location to store the backup.
    user -- a string containing the user profile name.
    backupLocations -- a dictionary containing the locations to backup.
    exclusions -- a list of exclusion patterns.
    
    """
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
    try:
        settings = readXML("wonderbackup.xml")
        messages = getMessages(readXML("localizations.xml"), language)
    except Exception:
        print messages['error']['files-missing'] + "\n"
        exit()
# Messages are in the format (backup_wizard, backup_options, dialogs, prompts, 
#                             summary, welcome)
    try:
        exclusions = getExclusions(settings)

    # Welcome Message
        print messages['welcome']['welcome'] #Welcome Message
    # Backup Type
        backupType = selectBackupType(messages) 
    # Select Source
        sourceDirectory = selectSource(messages, backupType)
        locations = getLocations(settings, detectOS(sourceDirectory)['family'], 
                                 detectOS(sourceDirectory)['version'])
    # Select Target
        targetDirectory = selectTarget( messages )
    # Select User
        user = selectUser( messages, sourceDirectory )
    # Select Backup Locations
        backupLocations = selectBackupLocations(messages, sourceDirectory, user, 
                                                locations)
    # Select Exclusions
        selectedExclusions = selectExclusions( messages, exclusions )
    # Start the Backup Progress
        startBackup(messages, backupType, sourceDirectory, targetDirectory, user, 
                    backupLocations, selectedExclusions )
    except KeyboardInterrupt:
        print "\n\n" + messages['error']['user-abort'] + "\n\n"
