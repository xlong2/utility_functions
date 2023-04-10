import re

from import_libs import *
# iterate through each python script
def return_python_files(filepath_obj):
    if filepath_obj.is_file():
        print(filepath_obj.path)
        filename = Path(filepath_obj.path).name
        filename_stem, filename_ext = ".".join(filename.split(".")[:-1]), filename.split(".")[-1]
        if  filename_ext == ".py":

            if len(filename_stem)==1 and filename_stem.isalpha():
                return filepath_obj, filename_stem




def find_files_to_be_sorted():
    print(" directory path is current directory")
    file_objs = [return_non_python_files(filepath_obj) for filepath_obj in os.scandir(".") if return_non_python_files(filepath_obj) is not None]
    for each_file_obj, each_file_stem in file_objs:
        with open(each_file_obj.path, 'r') as file:
            each_file_lines = file.readlines()
        if len(each_file_lines)<1:
            continue
        functions_dict_record = {}
        for each_line in each_file_lines:
            if re.search("^def ", each_line):
                function_name = each_line.replace("def ","")#
                functions_dict_record[function_name]= []
                functions_dict_record[function_name].append(each_line)
            else:
                functions_dict_record[function_name].append(each_line)


        # sort function names alphabetically

