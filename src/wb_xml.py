# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# wb_xml.py
#
# Contains the functions for the XML processing.
#
# Modified by Sean Davis on October 18, 2010
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

def writeXML(tree, filename):
    print "Not Yet Implemented"
