# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wbXML.py
#
# Contains the functions for the XML processing.
#
# Modified by Sean Davis on December 7, 2010
# ---------------------------------------------------------------------------- #

import os
from xml.etree import ElementTree as ET


def readXML(filename):
    """Return the Tree of the XML file.
    
    Keyword arguments:
    filename -- a string containing a valid filename.
    
    """
    xml_file = os.path.abspath(filename)
    xml_file = os.path.dirname(xml_file)
    xml_file = os.path.join(xml_file, filename)

    try:
           tree = ET.parse(filename)
    except Exception, inst:
           print "Unexpected error opening %s: %s" % (xml_file, inst)
    
    return tree
    
def getLocations( xmldoc, osFamily, osVersion ):
    """Returns a dictionary containing the OS-specificbackup locations.
    
    Keyword arguments:
    xmldoc -- an object of ElementTree.
    osFamily -- a string containing the family of the operating system.
    osVersion -- a string containing the version of the operating system.
    
    """
    allLocations = xmldoc.find('.//backup_locations').getchildren()
    locationDict = {}
    for i in range( len(allLocations) ):
        if allLocations[i].attrib['family'] == osFamily and allLocations[i].attrib['version'] == osVersion:
            for j in range( len(allLocations[i]) ):
                locationDict[allLocations[i][j].attrib.get('name')] = allLocations[i][j].text
    return locationDict
    
def getExclusions( xmldoc ):
    """Return a dictionary containing the exclusions defined in the xmldoc.
    
    Keyword arguments:
    xmldoc -- an object of ElementTree.
    
    """
    allExclusions = xmldoc.find('.//exclusion_definitions').getchildren()
    exclusionDict = {}
    typeList = []
    for i in range( len(allExclusions) ):
        exclusionDict[allExclusions[i].attrib.get('category')] = allExclusions[i].text.split(',')
    return exclusionDict
    
def getMessages( xmldoc, language ):
    """Return a dictionary (of dictionaries) for each category (and message 
    types) defined in the language of the xmldoc.
    
    Keyword arguments:
    xmldoc -- an object of ElementTree.
    
    Dictionary keys:
    (Defined by the XML document.)
    
    """
    allLanguages = xmldoc.findall('.//locale')
    messageDict = {}
    for i in range( len(allLanguages) ):
        if allLanguages[i].attrib.get('lang') == language:
            for j in range( len(allLanguages[i]) ):
                if j == 0:
                    dictionary = {}
                    previousCategory = allLanguages[i][j].attrib.get('category')
                if allLanguages[i][j].attrib.get('category') != previousCategory:
                    messageDict[allLanguages[i][j-1].attrib.get('category')] = dictionary
                    dictionary = {}
                    previousCategory = allLanguages[i][j].attrib.get('category')
                dictionary[allLanguages[i][j].attrib.get('name')] = allLanguages[i][j].text
            messageDict[allLanguages[i][j].attrib.get('category')] = dictionary
        return messageDict