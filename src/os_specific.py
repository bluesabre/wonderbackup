from platform import uname
from os import getenv
from os.path import isdir

def get_os():
    return [uname()[0], uname()[2]]

def get_logged_in():
    if get_os()[0] == "Windows":
        return getenv("USERNAME")
    else:
        return getenv("USER")

def check_valid_location( location ):
    if isdir(location):
        return True
		
def get_user_locations( username ):
    if get_os()[0] == "Windows":
        if get_os()[1] == "Vista" or get_os()[1] == "7":
            profile = "C:\\Users\\" + username + "\\"
            locations = [("Desktop", profile + "Documents\\"), ("Documents", profile + "Documents\\"), ("Favorites", profile + "Favorites\\"), ("Firefox Profiles", profile + "AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"), ("Music", profile + "Music\\"), ("Pictures", profile + "Pictures\\"), ("Videos", profile + "Videos\\")]
        else:
            profile = "C:\\Documents and Settings\\" + username + "\\"
            locations = [("Desktop", profile + "Desktop\\"), ("Favorites", profile + "Favorites"), ("Firefox Profiles", profile + "Application Data\\Mozilla\\Firefox\\Profiles\\"), ("My Documents", profile + "My Documents\\")]
    elif get_os()[0] == "Linux":
        profile = "/home/" + username + "/"
        locations = [("Desktop", profile + "Desktop/"), ("Documents", profile + "Documents/"), ("Music", profile + "Music/"), ("Mozilla (Firefox and Thunderbird) Profiles", profile + ".mozilla/"), ("Pictures", profile + "Pictures/"), ("Videos", profile + "Videos/")]
    else:
        profile = "/Users/" + username + "/"
        locations = [("Desktop", profile + "Desktop/"), ("Documents", profile + "Documents/"), ("Movies", profile + "Movies/"), ("Music", profile + "Music/"), ("Pictures", profile + "Pictures/")]
    all_locations = []
    for each in locations:
        if isdir(each[1]):
            all_locations.append(each)
    return all_locations
