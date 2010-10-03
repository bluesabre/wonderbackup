#!/bin/python
from output_functions import *

from os_specific import *

print "__            __\n\ \    __    / /\n \ \  /  \  / /\n  \ \/ /\ \/ /\n   \__/  \__/ONDER BACKUP\nDemo 1 - Tuesday, October 5, 2010\n"
print "What would you like to backup today?"
answer = raw_input(" 1. Documents\n 2. Pictures\n 3. Videos\n 4. Desktop \n 5. Everything\n 6. Custom\n 7. Exit\n\nEnter your selection: ")

print "The following backup options are available:"
for item in get_user_locations(get_logged_in()):
    print item[0]
