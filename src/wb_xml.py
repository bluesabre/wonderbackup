# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wb_xml.py
#
# Contains the functions for the XML processing.
#
# Modified by Sean Davis on November 2, 2010
# ---------------------------------------------------------------------------- #

from xml.etree import ElementTree as ET
import os

def readXML(filename):
    """readXML( string filename ) -> ElementTree
    
    Returns the Tree of the XML file.
    
    return ElementTree.tree"""
    xml_file = os.path.abspath(filename)
    xml_file = os.path.dirname(xml_file)
    xml_file = os.path.join(xml_file, filename)

    try:
           tree = ET.parse(filename)
    except Exception, inst:
           print "Unexpected error opening %s: %s" % (xml_file, inst)
    
    return tree

def get_backup_locations(tree):
    """get_backup_locations( ElementTree tree ) -> list

    Returns in list format, the backup locations from the XML file.
    The format is as follows:
    Each item is a tuple that first has the Operating System version:
     ex. [{'family':'windows', 'version':'xp,2003'}, ...
    And then the backup locations:
     ex.  ({'name':'Desktop'}, '%USERPROFILE%\\\\Desktop'), ... ]

    return list"""
    tree_locations = tree.find('.//backup_locations').getchildren()
    location_list = []
    locations = []
    for i in range(len(tree_locations)):
        locations.append([])
        locations[i].append(tree_locations[i].attrib)
        location_list = []
        location_list = tree_locations[i].getchildren()
        for j in range(len(location_list)):
            locations[i].append((location_list[j].attrib, location_list[j].text))
    return locations

def simple_locations(xml_tree, family, version):
    """simple_locations( ElementTree.tree, string family, string version ) -> list

    Returns the backup locations from the xml_tree for the specified operating system family and version.

    return list simple"""
    locations = get_backup_locations(xml_tree)
    simple = []
    for i in range(len(locations)):
        if locations[i][0]['family'] == family and locations[i][0]['version'] == version:
            for j in range(1,len(locations[i])):
                simple.append( [locations[i][j][0].values(),locations[i][j][1]] )
    return simple

def get_exclusions(tree):
    """get_exclusions( ElementTree tree ) -> list

    Returns in list format, the file exclusions from the XML file.
    The format is as follows:
    Each item is a tuple that first has the exclusion category and type:
     ex. [{'category': 'Music', 'type': 'extension'}, ...
    And then the exclusions:
     ex.  'aac,aiff,ape,asx,au,aup,band,cdda,cust,dwd,flac, ...']

    return list"""
    tree_exclusions = tree.find('.//exclusion_definitions').getchildren()
    exclusions = []
    for i in range(len(tree_exclusions)):
        exclusions.append([tree_exclusions[i].attrib, tree_exclusions[i].text])
    return exclusions

def get_messages(tree, language):
    """get_messages(ElementTree tree, string language) -> list

    Returns all of the messages for the specified language in the following 
    format: (backup_wizard, backup_options, dialogs, prompts, summary, welcome, about)

    return (backup_wizard, backup_options, dialogs, prompts, summary, welcome, about)"""
    lang = language
    lang_index = -1
    list_languages = tree.findall('.//locale')
    for i in range(len(list_languages)):
        if list_languages[i].attrib.get('lang') == language:
            lang_index = i
    if lang_index == -1:
        print "Language not found in localizations file. Defaulting to English."
        lang = 'en'
    languageSpecific = list_languages[lang_index]
    backup_wizard = []
    backup_options = []
    dialogs = []
    prompts = []
    summary = []
    welcome = []
    about = []
    for i in range(len(languageSpecific)):
        category = languageSpecific[i].attrib.get('category')
        name = languageSpecific[i].attrib.get('name')
        text = languageSpecific[i].text
        if category == 'backup':
            backup_wizard.append({name:text})
        elif category == 'backup-option':
            backup_options.append({name:text})
        elif category == 'dialog':
            dialogs.append({name:text})
        elif category == 'prompt':
            prompts.append({name:text})
        elif category == 'summary':
            summary.append({name:text})
        elif category == 'welcome':
            welcome.append({name:text})
        elif category == 'about':
            about.append({name:text})
        else:
            print "Unknown"
    return (backup_wizard, backup_options, dialogs, prompts, summary, welcome, about)

def get_message(message_list, name):
    """get_message( list message_list, string name ) -> string

    Returns the message from the message list.  Used with XML processing.

    return string"""
    for i in message_list:
        if i.keys()[0] == name:
            return i.get(name)

def writeXML(tree, filename):
    print "Not Yet Implemented"
    return False
