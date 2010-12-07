# ---------------------------------------------------------------------------- #
# Wonder Backup - http://wonderbackup.sourceforge.net/
# setup.py
#
# Contains the setup program for distribution using py2app or py2exe.
#
# Modified by Sean Davis on December 7, 2010
# ---------------------------------------------------------------------------- #

"""
py2app/py2exe build script for Wonder Backup

Usage (Mac OS X):  ## Not yet tested
    python setup.py py2app --resources ico16.ico,Icon.png,license.txt,localizations.xml,wonderbackup.xml
    
Usage (Windows):
    python setup.py py2exe
"""


import sys

if sys.platform == 'darwin':
    from setuptools import setup
    setup(
        app=["wbGUI.py"],
        setup_requires=["py2app"],
    )

elif sys.platform == 'win32':
    from distutils.core import setup
    import py2exe

    setup(
        # The first three parameters are not required, if at least a
        # 'version' is given, then a versioninfo resource is built from
        # them and added to the executables.
        version = "1.0 \"Stable One\"",
        description = "Wonder Backup is an open source, Python-powered, operating system independent backup solution for use in scenarios from end-users to enterprise solutions.",
        name = "Wonder Backup",

        # targets to build
        windows = [
            {
                "uac_info": "requireAdministrator",
                "script": "wbGUI.py",
                "icon_resources": [(0, "Icon.ico")]
            }
        ],
        console = [
            { 
                "uac_info": "requireAdministrator",
                "script": "wbCLI.py"
            }
                ],
        )