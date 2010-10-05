#!/bin/python
from output_functions import *

from all_functions import *

print dir()

print "__            __\n\ \    __    / /\n \ \  /  \  / /\n  \ \/ /\ \/ /\n   \__/  \__/ONDER BACKUP\nDemo 1 - Tuesday, October 5, 2010\n"

locations = get_user_locations( get_logged_in() )

backups_available = ""
total = 0
for item in locations:
    backups_available += (" " + str(total+1) + ". " + str(item[0]) + "\n")
    total += 1

print "What would you like to backup today?"
answer = input( backups_available + " " + str(total+1) + ". Exit\n\nEnter your selection: ")

if answer == total+1:
    exit()

target = raw_input( "Where would you like to back these files up?\n " )

exclusions = raw_input( "Are there any filetypes that you would like to exclude? [default]: " )

mkdir(target + locations[answer-1][0])
copy_multiple( locations[answer-1][1], target + locations[answer-1][0], [".DS_STORE"] )
