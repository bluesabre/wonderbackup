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

def print_message(category, name, windowsize=80):
    """print_message(string category, string name, int windowsize)

    Prints a message as is defined in an XML document under the given category and name"""
    for i in range(len(messages)):
        if messages[i][0]['category'] == category and messages[i][0]['name'] == name:
            print messages[i][1]

def welcome_message(message_list):
    """welcome_message( list message_list )

    Prints the welcome message."""
    print_message('welcome', 'welcome')

def backup_type(message_list):
    """backup_type( list message_list ) -> int

    Runs the user through the backup type selection, returning the selection as an integer.

    return int answer"""
    print_message('backup', 'backup-type')
    answer = 0
    while answer < 1 or answer > 3:
        answer = input("1. Local Backup\n2. External Backup\n3. Load Preconfigured Backup\n\nEnter your selection: ")
    return answer

def select_source(message_list, answer):
    """select_source( list message_list, int answer ) -> string

    Runs the user through the backup source selection, if necessary, returning the location as a string.

    return string location"""
    # Need detect os here.
    if answer == 1:
        return local_location
    else:
        print_message('backup', 'select-source')

#----------------------------------------------------------------------
if __name__ == "__main__":
    xml_doc = readXML("wonderbackup.xml")
    locations = get_backup_locations(xml_doc)
    exclusions = get_exclusions(xml_doc)
    messages = get_messages(xml_doc)

    welcome_message(messages)

    ans = backup_type(messages)
    select_source(messages, ans)
