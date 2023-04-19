import os

from r import read_directory_recursive, read_file
package_directory = "./a_directory"
all_files = read_directory_recursive(package_directory)
# 

bundled_python_files = {}
copy_dir = f"{os.path.basename(package_directory)}_copy/"
os.system(f"mkdir {copy_dir}")

for root, subdirs, files in os.walk(package_directory):
    relative_dir = copy_dir + root.replace(package_directory+"/", "")+'/'
    python_files = [x for x in files if ".py" in x]
    os.system(f"mkdir {relative_dir}")



for root, subdirs, files in os.walk(package_directory):
    python_files = [x for x in files if ".py" in x]
    root_ = root +"/"
    if len(python_files)>0:
        bundled_python_files[root_] = [root_+x for x in python_files]

        
    
import re

python_files = sum([y for x,y in bundled_python_files.items()],[])
all_files = [x for x in python_files if ".py" in x]
functions_dict_rec = []
functions_by_filename = {}
function_definition_appearance_in_files = {}
import tqdm
for each_file in tqdm.tqdm(all_files):
    try:
        file_lines = read_file(each_file)
    except:
        continue
    if len(file_lines )<1:
        continue
    functions_dict_record = {}
    first_function_found = False
    recording_switch = True  # becomes False only when it is reading class code
    singlequote_recording_switch = True
    doublequote_recording_switch = True
    pair_singlequote_counter = 0
    pair_doublequote_counter = 0

    other_lines =[]
    for each_line in file_lines:

        if "Converts a class" in each_line:
            print("this")
        each_line_lstrip = each_line.lstrip()
        if re.search("^class", each_line):
            recording_switch = False
            continue
        if re.search("^#", each_line_lstrip):
            continue
        if re.search("'''" ,each_line_lstrip):
            length = len(re.findall("'''", each_line_lstrip))

            pair_singlequote_counter+=length
            if pair_singlequote_counter % 2 ==1:
                singlequote_recording_switch = False
            elif pair_singlequote_counter % 2==0:
                singlequote_recording_switch = True
                pair_singlequote_counter = 0 
            continue
        if re.search("\"\"\"" ,each_line_lstrip):
            length = len(re.findall("\"\"\"", each_line_lstrip))

            pair_doublequote_counter +=length
            if pair_doublequote_counter % 2 == 1:
                doublequote_recording_switch = False
            elif pair_doublequote_counter % 2 == 0:
                doublequote_recording_switch = True
                pair_doublequote_counter = 0
            continue
        if (re.search("^import", each_line) or re.search("^from ",each_line)) and doublequote_recording_switch and singlequote_recording_switch:
            if "import" not in functions_dict_record.keys():
                functions_dict_record["import"]= []
            functions_dict_record["import"].append(each_line)
            continue
        if ((not re.search("^ ",each_line)) and (not re.search("^from", each_line)) and (not re.search("^import",each_line))) and (not re.search("^def", each_line)):
            continue

        if re.search("^def ", each_line) and singlequote_recording_switch and doublequote_recording_switch:
            if not first_function_found:
                first_function_found = True

            function_name = each_line.replace("def","").replace(" ","").split("(")[0]#
            functions_dict_record[function_name]= []
            functions_dict_record[function_name].append(each_line)
            if function_name not in function_definition_appearance_in_files.keys():
                function_definition_appearance_in_files[function_name] = []
            function_definition_appearance_in_files[function_name].append(each_file)
            recording_switch = True
        elif singlequote_recording_switch and doublequote_recording_switch:
            if not first_function_found:
                continue

            if recording_switch:

                functions_dict_record[function_name].append(each_line)
    functions_dict_rec.append(functions_dict_record)
    functions_by_filename[each_file] = functions_dict_record
# combine all
keys_all = []
values_all = []
for each in functions_dict_rec:
    keys, values = each.keys(), each.values()
    keys_all = keys_all + [x for x in keys]
    values_all = values_all + [x for x in values]

# indexing all function names
all_functions_in_the_package = {}
for each_key, each_func in zip(keys_all, values_all):
    if each_key in all_functions_in_the_package.keys():
        continue
    else:
        all_functions_in_the_package[each_key] = each_func


def if_a_in_b(a, b):
    """
    @parameter a: a string
    @parameeter b: a list of string
    """

    for each in b:
        if a in each:
            return True
        else:
            continue



function_reference_frequency_counter = {}
function_reference_file_appearance = {}
import tqdm
for file_name, functions_in_the_file in tqdm.tqdm(functions_by_filename.items()):
    to_remove = []
    for each_func_name, each_func in tqdm.tqdm(functions_in_the_file.items()):
        # if the function quote other functions in the package 
        if each_func_name == "import":
            continue
        pass_flag = True
        for each_key in keys_all:
            if each_func_name==each_key:
                continue
                
            else:
                if if_a_in_b(each_key, each_func):
                    if each_key not in function_reference_frequency_counter.keys():
                        function_reference_frequency_counter[each_key] = 1
                        function_reference_file_appearance[each_key]=[]
                        function_reference_file_appearance[each_key].append(file_name)
                    else:
                        function_reference_frequency_counter[each_key] += 1
                        function_reference_file_appearance[each_key].append(file_name)
                    continue
                    pass_flag = False

        if not pass_flag:  # remove the function in the dictionary if it uses other functions
            to_remove.append(each_func_name)

    for each_func_name in to_remove:
        del functions_in_the_file[each_func_name]
    functions_by_filename[file_name] = functions_in_the_file  # reassign


function_reference_frequency_counter_sorted = {k:v  for k, v in sorted(function_reference_frequency_counter.items(), key=lambda item: item[1],reverse=True)}
function_reference_file_appearance_sorted = {k:function_reference_file_appearance[k]  for k, v in sorted(function_reference_frequency_counter.items(), key=lambda item: item[1],reverse=True)}
function_definition_appearance_in_files_sorted = {k:v  for k, v in sorted(function_definition_appearance_in_files.items(), key=lambda item: len(item[1]),reverse=True)}


from w import write_to_file_append, write_to_file_overwrite

write_by_alphabets= True
write_into_alphabet_files = False
overwrite_directory = True
for each_file, functions_in_file in functions_by_filename.items():

    lines = sum([x for x in functions_in_file.values()],[])
    if len(lines)==0:
        continue
    if write_by_alphabets:
        functions_in_file_alphabetically = {k: v for k, v in
                                                       sorted(functions_in_file.items(),
                                                              key=lambda item: item[0], reverse=False)}
        lines = sum([x for x in functions_in_file_alphabetically.values()],[])

    relative_dir = copy_dir + each_file.replace(package_directory + "/", "") 
    if overwrite_directory and ("copy" in relative_dir or "Copy" in relative_dir):
        write_to_file_overwrite("", relative_dir)
    if not os.path.isfile(relative_dir):
        write_to_file_overwrite("",relative_dir)
    write_to_file_append(lines,relative_dir)
    print(relative_dir)

os.system("mkdir "+copy_dir + "func_reference_file_list/")
for each_func, file_list in function_reference_file_appearance_sorted.items():
    if overwrite_directory and ("copy" in copy_dir or "Copy" in copy_dir):
        file_list = [x +"\n" for x in file_list]
        write_to_file_overwrite(file_list, copy_dir+ "func_reference_file_list/"+each_func+".list")

os.system("mkdir "+copy_dir + "func_definition_file_list/")
for each_func, file_list in function_definition_appearance_in_files_sorted.items():
    if overwrite_directory and ("copy" in copy_dir or "Copy" in copy_dir):
        file_list = [x +"\n" for x in file_list]
        write_to_file_overwrite(file_list, copy_dir+ "func_definition_file_list/"+each_func+".list")


print("end of the script")



    
        
