
import pathlib
from pprint import pprint
import csv

# path to your desktop
path_to_desktop ="/mnt/d/New folder"

#create desktop path object
desktop_path = pathlib.Path(path_to_desktop)


# new dictionary
new_dict = {}

# establish the key pairs and their counts and store in a dictionary
for filepath in desktop_path.iterdir():
    #establish if the suffix is in the dict, if not append the dict with new key (suffix)
    if filepath.suffix not in new_dict.keys():
            new_dict[filepath.suffix] = 0
        
        
    # loop through the dict keys
    for key in new_dict.keys():
        #if suffix matches key, assign value of 1
        if filepath.suffix == key:
            new_dict[key] += 1


pprint(new_dict)          

#loop through the files and see which one exceeds 5
for key, value in new_dict.items():
    if value >= 5:
        # loop through all files in dekstop, filter filepaths to only those that resemble the key and are files and not directories
        for filepath in desktop_path.iterdir():
            if filepath.suffix == key and filepath.is_file():
                # create a new folder
                folder_name = key[1:] + "_subfolder"
                new_path = desktop_path.joinpath(folder_name)
                new_path.mkdir(exist_ok=True)
    
                #new path to each file
                new_filepath = new_path.joinpath(filepath.name)
        
                #move the files from the old path to the new path
                filepath.replace(new_filepath)
    

#store the desktop status

with open("desktop_status.txt", "a") as ds:
    ds.write(str(new_dict) + "\n")
