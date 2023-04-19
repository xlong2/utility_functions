def read_directory_recursive(directory):
    # read in the directory where the library to be extracted is
    files_all=[]
    for root, subdirs, files in os.walk(directory):
        files_all = files_all + [root+"/"+x for x in files]
    return files_all

def read_file(filepath):
    with open(filepath, "r") as the_file:
        lines = the_file.readlines()
        return lines

