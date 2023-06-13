import os
import json

def get_full_path_from_partial(partial_path):
    current_dir = os.getcwd()
    split_dir = current_dir.split(os.sep)
    split_partial = partial_path.split(os.sep)

    # Find the common path
    common_path = os.path.commonprefix([split_dir, split_partial])

    # Handle the case where there's no common path
    if not common_path:
        raise ValueError('No common path found')

    # Find the uncommon path from the partial path
    uncommon_path = os.sep.join(split_partial[len(common_path):])

    # Return the joined common and uncommon paths
    return os.path.join(os.sep.join(common_path), uncommon_path)

def find_files_with_extension(directory, extension):
    #Find all files in the directory with the given extension.
    found_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                found_files.append(os.path.join(root, file))
    return found_files

def read_deprecated_methods(deprecated_methods_file):
    with open(deprecated_methods_file, 'r') as f:
        deprecated_methods = f.read().splitlines()
    return deprecated_methods

def is_valid_json(file_path):
    """Check if a file contains valid JSON."""
    try:
        with open(file_path, 'r') as file:
            json.load(file)
        return True
    except Exception as e:
        print (file_path)

        print(type(e).__name__,str(e))
        return False

def read_json_file(json_file):
    with open(json_file, 'r', encoding = 'utf8') as f:
        #datas = f.read().splitlines()
        try:
            data = json.load(f)
        except:
            data = None
            print ("Fail to Read {0}",json_file)
    return data