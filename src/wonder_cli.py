# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wonder_cli.py
#
# Contains the functions for the command-line interface.
#
# Modified by Sean Davis on October 24, 2010
# ---------------------------------------------------------------------------- #
from wb_backup import *
from wb_file import *
from wb_os import *
from wb_xml import *

def truncate_directory( directory, size ):
    """truncate_directory( string directory, int size )

    Returns a string directory truncated to the given length size.

    return string directory"""
    if len(directory) > size-2:
        truncated = ""
        for i in range(len(directory)-size-2, len(directory)):
            truncated += directory[0]
    else:
        return directory

def terminal_filename( filename, fit_size ):
    """terminal_filename( string filename, int fit_size) -> string
    
    Returns a string of the filename designed to fit in the given amount of space.
    
    return string filename"""
    if len(filename) >= fit_size:
        extension = get_extension(filename)
        truncated = ""
        for i in range(fit_size-3-len(extension)):
            truncated += filename[i]
        truncated += "..."
        truncated += extension
        return truncated
    else:
        extended = ""
        for i in range(len(filename)):
            extended += filename[i]
        for i in range(fit_size - len(filename)):
            extended += " "
        return extended
        
def terminal_size( size, measurement ):
    """terminal_size( string size, string measurement ) -> string
    
    Returns a string of the file size in a format that fits six blocks.
    
    return string file_size"""
    if len(size) == 4:
        return size + measurement
    elif len(size) == 3:
        return "~" + size + measurement
    elif len(size) == 2:
        return "~" + size + " " + measurement
    else:
        return "~ " + size + " " + measurement
    
def terminal_modified( date ):
    """terminal_modified( string date ) -> string
    
    Returns a string of the modified date in the following format: MM/DD/YY
    
    return string modification_date"""
    return str(date[0]) + "/" + str(date[1]) + "/" + str(date[2])

def terminal_output( directory, files, size=79 ): #Size must be greater than 32.
    """terminal_output( string directory, list files, int size )
    
    Prints the files given in a format that is easy on the eyes and easy to follow."""
    if directory[len(directory)-1] != "/":
        directory += "/"
    title_size = truncate_directory(directory, size)
    title_upper = "o-"
    for i in range(len(title_size)):
        title_upper += "-"
    title_upper += "-o"
    print title_upper
    print "| " + title_size + " |"
    line = "o-"
    for i in range(size-24):
        line += "-"
    line += "-o--------o----------o"
    print line
    infoline = "| Filename"
    for i in range(size-32):
        infoline += " "
    infoline += " |  Size  | Modified |"
    print infoline
    print line
    for file in files:
        attrib = get_attributes( directory + str(file), str(file) )
        print "| " + terminal_filename(attrib[0], size-24) + " | "  + terminal_size(attrib[1][0], attrib[1][1]) + " | " + terminal_modified(attrib[2]) + " |"
    print line

def backup_type(message, local_backup_option, external_backup_option, preconfigured_backup_option, prompt):
    """backup_type( string message, string local_backup_option, string external_backup_option, string preconfigured_backup_option, string prompt ) -> int

    Runs the user through the backup type selection, returning the selection as an integer.

    return int answer"""
    print message
    answer = 0
    while answer < 1 or answer > 3:
        answer = input("1. " + local_backup_option + "\n2. " + external_backup_option + "\n3. " + preconfigured_backup_option + "\n\n" + prompt)
    return answer

def select_source(message, answer):
    """select_source( string message, int answer ) -> string

    Runs the user through the backup source selection, if necessary, returning the location as a string.

    return string location"""
    os = get_os()
    local_location = '/home/'
    if answer == 1:
        return (os, local_location)
    else:
        print message

def select_target( message, prompt ):
    """select_target( string message, string prompt ) -> string

    Returns the location that is entered by the user.  Checks for validity and adds necessary ending slashes.

    return string location"""
    print message
    location = "a"
    while not check_valid_location(location):
        location = raw_input(prompt + "\n ")
    if location[len(location)-1] != '/':
        location = location + "/"
    return location

from os import listdir
def select_user( message, prompt, source ):
    """select_user( string message, string prompt, string source ) -> string

    Returns the user profile selected for backup.

    return string profile"""
    print message
    users = listdir(source)
    for i in range(1,len(users)+1):
        print str(i) + ". " + users[i-1]
    ans = 0
    while ans < 1 or ans > len(users):
        ans = input(prompt)
    return users[ans-1]

def select_backup_locations( message, prompt, source, user, locations ):
    """select_backup_locations( string message, string prompt, string source, string user, list locations ) -> list

    Returns the list of backup locations to be backed up.

    return list answers"""
    print message
    answers = []
    for i in range(len(locations)):
        ans = ""
        while ans != 'y' and ans != 'n':
            ans = raw_input(prompt + locations[i][0][0] + "?\ny or n: ")
        if ans == 'y':
            answers.append([locations[i][0][0],str(source) + str(user) + str(locations[i][1])])
    return answers

def select_exclusions( message, prompt, exclusions ):
    """select_exclusions( string message, string prompt, list exclusions ) -> list

    Returns a list of two lists of file extensions and file names to be excluded, as selected by the user.

    return list exclusions"""
    print message
    extensions = []
    filenames = []
    for i in range(len(exclusions)):
        ans = ""
        while ans != 'y' and ans != 'n':
            ans = raw_input(prompt + exclusions[i][0]['category'] + "?\ny or n: ")
        if ans == 'y':
            ext = exclusions[i][1].rsplit(',')
            for j in range(len(ext)):
                if exclusions[i][0]['type'] == 'extension':
                    extensions.append(ext[j])
                else:
                    filenames.append(ext[j])
    extensions.sort()
    filenames.sort()
    return [extensions, filenames]


def start_backup( message, backup_details, type_text, type_answer, source_text, target_text, user_text, locations_text, exclusions_text, prompt, backup_type, source_directory, target_directory, user, backup_locations, exclusions ):
    """start_backup( list message_list, int backup_type, string source_directory, string target_directory, string user, list backup_locations, list exclusions )

    Confirms that all settings are correct and begins the backup program."""
    print message
    print backup_details
    print type_text + str(type_answer)
    print source_text + str(source_directory[1])
    print target_text + str(target_directory)
    print user_text + str(user)
    print locations_text + "\n"
    for i in (range(len(backup_locations))):
        print " " + backup_locations[i][1]
    print exclusions_text + "\n " + str(exclusions[0]) + "\n " + str(exclusions[1])
    raw_input(prompt)
    for i in range(len(backup_locations)):
        mkdir(target_directory + backup_locations[i][0])
        copy_multiple(backup_locations[i][1], target_directory+backup_locations[i][0], exclusions[0])
    


#----------------------------------------------------------------------
if __name__ == "__main__":
    """Main function, called when issuing a command 'python command'"""
    language = 'en'
    settings = readXML("wonderbackup.xml")
    messages = get_messages(readXML("localizations.xml"), language)
# Messages are in the format (backup_wizard, backup_options, dialogs, prompts, summary, welcome)
    locations = get_os_backup_locations(settings)
    exclusions = get_exclusions(settings)

# Welcome Message
    print get_message(messages[5], 'welcome') #Welcome Message
# Backup Type
    b_type = backup_type(get_message(messages[0],'backup-type'), get_message(messages[1],'local'), get_message(messages[1],'external'), get_message(messages[1],'preconfigured'), get_message(messages[3],'enter-selection')) 
# Select Source
    source = select_source(get_message(messages[0],'select-source'), b_type)
# Select Target
    target = select_target(get_message(messages[0],'select-target'), get_message(messages[3],'enter-location') )
# Select User
    user = select_user( get_message(messages[0],'select-user'), get_message(messages[3],'select-profile'), source[1] )
# Select Backup Locations
    b_locations = select_backup_locations( get_message(messages[0],'select-locations'), get_message(messages[3],'to-backup'), source[1], user, locations )
# Select Exclusions
    exclude = select_exclusions( get_message(messages[0],'select-exclusions'), get_message(messages[3],'to-exclude'), exclusions )
# Start the Backup Progress
    start_backup(get_message(messages[0],'proceed'), get_message(messages[4],'details'), get_message(messages[4],'type'), b_type, get_message(messages[4],'source'), get_message(messages[4],'target'), get_message(messages[4],'profile'), get_message(messages[4],'locations'), get_message(messages[4],'exclusions'), get_message(messages[4],'proceed'), b_type, source, target, user, b_locations, exclude )
