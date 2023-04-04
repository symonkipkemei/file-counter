
import pathlib
from pprint import pprint
import sqlalchemy as s
import os
import csv


#create desktop directory_path object
def get_path(desktopath:str):
    try:
        path = pathlib.Path(desktopath)
    except FileNotFoundError as e:
        print("Incorrect path address to the folder")

    return path
  

def get_file_data(directory_path:pathlib.Path):
    """Abstract all file data in that particular directory

    Args:
        directory_path (Path): directory_path to the desktop

    Returns:
        dict: A dictionary with all files present in that directory/desktop directory
    """
    # avaialable file types
    file_data = []

    # loop throught the primary directory_path, filter files only.
    for filepath in directory_path.iterdir():
        if filepath.is_file():
            #naming is consistent with the data base
            data = {"file_name":filepath.stem ,"file_path":filepath.name ,"file_type":filepath.suffix}
            file_data.append(data)

    return file_data


def file_type_count(directory_path:pathlib.Path):

    """Count all the files of the same type

    Returns:
        dict: suffixes and their count
    """
    # abstract all file types and  aggregate their numbers

    data = {}

    # Abstract all the file types present in the directory
    for filepath in directory_path.iterdir():
        if filepath.is_file():
            if filepath.suffix not in data.keys():
             data[filepath.suffix] = 0
    
    #Count all the file types present in the directory
    for filepath in directory_path.iterdir():
        # loop through the dict keys
        for key in data.keys():
            #if suffix matches key, assign value of 1
            if filepath.suffix == key:
                data[key] += 1

    return data


def clean_directory(directory_path:pathlib.Path,file_type:dict,limit:int):
    """Abstracts all files in a directory and organises into subfolders based on their type

    Args:
        directory_path (pathlib.Path): path to the directory
        file_type (dict): file types and their counts
        limit (int): the maximum type of files in the directory, more than this gets cleaned
    """
    #loop through the files and see which one exceeds the limit
    for key, value in file_type.items():
        if value >= limit:
            # loop through all files in dekstop, filter filepaths to only those that resemble the key and are files and not directories
            for filepath in directory_path.iterdir():
                if filepath.suffix == key and filepath.is_file():
                    # create a new folder
                    folder_name = key[1:] + "_subfolder"
                    new_path = directory_path.joinpath(folder_name)
                    new_path.mkdir(exist_ok=True)
    
                    #new directory_path to each file
                    new_filepath = new_path.joinpath(filepath.name)
        
                    #move the files from the old directory_path to the new directory_path
                    filepath.replace(new_filepath)


    
if __name__ == "__main__":
    pass