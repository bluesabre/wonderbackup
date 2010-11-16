# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wbXML.py
#
# Contains the functions for the XML processing.
#
# Modified by Sean Davis on November 14, 2010
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
    
def getLocations( xmldoc, osFamily, osVersion ):
    """getLocations( ElementTree xmldoc, string osFamily, string osVersion ) -> dict
    
    Returns a dictionary containing the backup locations for the osFamily and osVersion defined in the xmldoc.
    
    return dict"""
    allLocations = xmldoc.find('.//backup_locations').getchildren()
    locationDict = {}
    for i in range( len(allLocations) ):
        if allLocations[i].attrib['family'] == osFamily and allLocations[i].attrib['version'] == osVersion:
            for j in range( len(allLocations[i]) ):
                locationDict[allLocations[i][j].attrib.get('name')] = allLocations[i][j].text
    return locationDict
    
def getExclusions( xmldoc ):
    """getExclusions( ElementTree xmldoc ) -> dict
    
    Returns a dictionary containing the exclusions defined in the xmldoc.
    
    return dict"""
    allExclusions = xmldoc.find('.//exclusion_definitions').getchildren()
    exclusionDict = {}
    typeList = []
    for i in range( len(allExclusions) ):
        exclusionDict[allExclusions[i].attrib.get('category')] = allExclusions[i].text.split(',')
    return exclusionDict
    
def getMessages( xmldoc, language ):
    """getMessages( ElementTree xmldoc, language ) -> dict
    
    Returns a dictionary (of dictionaries) for each category (and message types)
    defined in the language of the xmldoc.
    Example:
     > messages = getMessages( readXML("wonderbackup.xml"), 'en' )
     > print messages['about']['description']
    
    return dict messageDict"""
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

def writeXML(tree, filename):
    print "Not Yet Implemented"
    return False
