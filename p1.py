"""
    Program: p1.py
    Author: Khann Mean
    Date: 2019-04-02
    Searches deep inside a directory structure, looking for duplicate file.
    Duplicates aka copies have the same content, but not necessarily the same name.
"""

import p1utils
import time
import os


def search(file_list):
    """
    Search a file list to identify the duplicates in the file list.

    Parameters:
    file_list (list): The list of files from a directory.

    Returns:
    list: returns a dictionary list of the duplicate files

    """

    count = 0
    file_list_dict = {}
    dupelist = []

    # sort the file list
    file_list.sort()
    # loop through the file list and look for duplicates
    for file1 in file_list:
        count = count + 1
        dupelist.clear()
        # compare to all files except itself and the last file in the list
        for file2index in range(count, len(file_list) - 1):
            file2 = file_list[file2index]
            # if files are the same
            if p1utils.compare(file1, file2) == True:
                # found a duplicate, add into a list
                dupelist.append(file2)

        # store the duplicate file list into the dictionary
        file_list_dict[file1] = dupelist.copy()

    return file_list_dict

def faster_search(file_list):
    """
    A faster search using pre-calculated hashes to identify the duplicates in the file list.

    Parameters:
    file_list (list): The list of files from a directory.

    Returns:
    list: returns a dictionary list of the duplicate files

    """

    count = 0
    file_list_hash = {}
    file_list_dict = {}
    dupelist = []

    # sort the file list
    file_list.sort()

    for filename in file_list:
        # create a list of file hashes from the files and store them
        file_list_hash[filename] = p1utils.hash_file(filename)

    # loop through the file list and look for duplicates
    for file1 in file_list:
        count = count + 1
        dupelist.clear()
        # compare to all files except itself and the last file in the list
        for file2index in range(count, len(file_list) - 1):
            file2 = file_list[file2index]
            # if the pre-calculated file hash values are the same
            if (file_list_hash[file1] == file_list_hash[file2]):
                # found a duplicate, add into a list
                dupelist.append(file2)

        # store the duplicate file list into the dictionary
        file_list_dict[file1] = dupelist.copy()


    return file_list_dict


def report(file_list_dict):
    """
    Report the results from search and display the list of duplicates and the list of duplicates
    that take up the most space.

    Parameters:
    file_list (list): The list of files from a directory.

    Returns:
    None.

    """

    # Return a error message if the diction is empty
    if not file_list_dict:
        print("Error: Empty file dictionary found.")
        return

    # find the file with max duplicates
    maxdupecount = 0
    maxdupefilename = ""
    for filename in file_list_dict:
        filenamedupelist = file_list_dict.get(filename)
        # if length of the duplicate list is greater than the max duplicate count set max
        if len(filenamedupelist) > maxdupecount:
            maxdupecount = len(filenamedupelist)
            maxdupefilename = filename

    # find the file with the most disk space in the duplicate list in the dictionary
    maxsizefilename = ""
    maxsizetotalspace = 0

    for filename in file_list_dict:
        filesize = os.path.getsize(filename)
        # get the number of duplicate files for filename
        filedupecount = len(file_list_dict.get(filename))
        # if the total space of the duplicate files is greater than the total max
        if (filesize * filedupecount > maxsizetotalspace):
            # save the new max duplicate space file info
            maxsizefilename = filename
            maxsizetotalspace = filesize * filedupecount

    # display the list of duplicate files
    print("The file with the most duplicates is:")
    print(str(maxdupefilename))
    print("Here are its " + str(maxdupecount) + " copies:")
    filedupelist = file_list_dict.get(maxdupefilename)
    for filename in filedupelist:
        print(str(filename))

    # display the list of files that take up the most space.
    print("")
    print("The most disk space (" + str(maxsizetotalspace) + ") could be recovered, by deleting copies of this file:")
    print(maxsizefilename)
    print("Here are its " + str(len(file_list_dict.get(maxsizefilename))) + " copies:")
    filedupelist = file_list_dict.get(maxsizefilename)
    for filename in filedupelist:
        print(str(filename))
    print("")

    pass


path = "." + os.sep + "smallset"  # starting point of the search, e.g. the smallset or the fullset

# find all files in the provided directory
files = p1utils.all_files(path)
print("Number of files found: ", len(files))

# measure how long the search and reporting takes:
t0 = time.time()
report(search(files))
print("Runtime: {:.2f} secs".format(time.time() - t0))

print(" .. and now w/ a faster search implementation:")
t0 = time.time()
report(faster_search(files))
print("Runtime: {:.2f} secs".format(time.time() - t0))
