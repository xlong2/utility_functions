def write_to_file_overwrite(lines, filepath):
    with open(filepath, 'w') as the_file:
        the_file.write(lines)

def write_to_file_append(lines, filepath):
    with open(filepath,"a") as the_file:
        the_file.write(lines)