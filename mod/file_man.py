import sys, os
from tkinter.filedialog import askdirectory

main_folder = os.getcwd()

_search_file_method = 0
#0: full path of first match
#1: boolean
#2: multiple matches >>>int
#3: multiple matches >>>list(paths)

first_path = None
#used for the first method search(file_name, path) to get the path of the first result from path

existence = False
#boolean used in exists(file_name, path) to know if file_name exists in the path

n = 0
#number used in file_n(file_name, path) to define how much there are files named file_name in the path

paths = []
#list used in search_files(file_name, path) containing the path of every file named file_name from path

def access_dir():
    folder = askdirectory()
    if folder == "":
        return None
    global main_folder
    main_folder = ""
    for char in folder:
        if char == '/':
            main_folder += chr(0x5C)
        else:
            main_folder += char
    return None

def exists(file_name: str, path = main_folder):
    global _search_file_method
    global existence
    _search_file_method = 1
    searching(file_name, path)
    e = existence
    existence = False
    return e

def file_n(file_name: str, path = main_folder):
    global _search_file_method
    global n
    _search_file_method = 2
    searching(file_name, path)
    _search_file_method = 0
    number = n
    n = 0
    return number

def search_files(file_name: str, path = main_folder):
    global _search_file_method
    _search_file_method = 3
    global paths
    searching(file_name, path)
    _search_file_method = 0
    if len(paths) == 0:
        return None
    p = paths
    paths = []
    if len(p) == 1:
        return p[0]
    return p

def search(file_name, path = main_folder, create = 'n'):
    searching(file_name, path)
    global first_path
    f = first_path
    first_path = None
    if create == 'y':
        if f == None:
            with open(file_name, 'w+'):
                pass
            search(file_name, path)
    return f

def searching(file_name: str, path = main_folder):
    if type(file_name) != str:
        raise ValueError(f"{file_name} has to be a string")
    global _search_file_method
    global first_path
    try:
        files = os.listdir(path)
    except:
        return None
    for file in files:
        if file == file_name and _search_file_method == 0:
            first_path = path + chr(0x5C) + file_name
            return None
        elif file == file_name and _search_file_method == 1:
            global existence
            existence = True
            _search_file_method = 0
            return None
        elif file == file_name and _search_file_method == 2:
            global n
            n += 1
            return None
        elif file == file_name and _search_file_method == 3:
            global paths
            paths.append(path + chr(0x5C) + file_name)
            return None
        file_type = 'dir'
        for char in file:
            if char == '.':
                file_type = 'file'
        if file_type == 'dir' and _search_file_method in [2, 3]\
            or file_type == 'dir' and _search_file_method == 1 and existence == False\
            or file_type == 'dir' and _search_file_method == 0 and first_path == None:
                try:
                    searching(file_name, path + chr(0x5C) + file)
                except:
                    pass
    return None