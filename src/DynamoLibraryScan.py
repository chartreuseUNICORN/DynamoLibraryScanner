import os
import json
import csv
import xml.etree.ElementTree as ET
import argparse

def read_deprecated_methods(deprecated_methods_file):
    with open(deprecated_methods_file, 'r') as f:
        deprecated_methods = f.read().splitlines()
    return deprecated_methods

def read_json_file(json_file):
    with open(json_file, 'r', encoding = 'utf8') as f:
        #datas = f.read().splitlines()
        data = json.load(f)
    return data

def report_package_usage (data):
    depends = data.get('NodeLibraryDependencies','')
    packages = list(filter(lambda x: x.ReferenceType == 'Package',depends))
    report = [(package.Name,package.Version,len(package.Nodes)) for package in packages]
    return report

def search_deprecated_methods( data, deprecated_methods):
    searchResult = []
    name = data.get('Name','')
    nodes = data.get('Nodes', [])
    for node in nodes:
        function_signature = node.get('FunctionSignature', '')
        node_type = node.get('NodeType','')
        if node_type == 'FunctionNode':
            if function_signature in deprecated_methods:
                searchResult.append(function_signature) 
    #if deprecated_found:
    #    print ("{0}: Found {1} Deprecated Methods".format(name,len(deprecated_found)))
    return searchResult

def search_python_nodes (data):
    searchResult = []
    nodes = data.get('Nodes',[])
    for node in nodes:
        node_type = node.get('NodeType','')
        if node_type == 'PythonScriptNode':
            engine = node.get('Engine','')
            if engine == 'IronPython2':
                searchResult.append(node_type)
    return searchResult

def search_code_blocks (data):
    searchResult = []
    nodes = data.get('Nodes',[])
    for node in nodes:
        node_type = node.get('NodeType','')
        if node_type == 'CodeBlockNode':
            searchResult.append(node_type)
    return searchResult

def search_dependencies (data):
    # TODO: implement node lookup to include unique node names used in the script
    searchResult = []
    deps = data.get('NodeLibraryDependencies',[])
    for d in deps:
        dType = d.get('ReferenceType','')
        if dType == "Package":    
            searchResult.append((d.get('Name',''),d.get('Version',''),d.get('Nodes',[])))
    return searchResult

def find_files_with_extension(directory, extension):
    """Find all files in the directory with the given extension."""
    found_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                found_files.append(os.path.join(root, file))
    return found_files

def search_file_methods (json_file, deprecated_methods):    
    data = read_json_file(json_file)
    name = data.get('Name','')
    searchResults = search_deprecated_methods(data, deprecated_methods)
    #print("Result: {0}".format(searchResults))
    return (name,list(set(searchResults)))

def write_data_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Path", "Node Names"])  # writing the header
        for item in data:
            writer.writerow(item)

def generate_package_report (reports):

    pack_dict = {}
    for report in reports:
        detailed_report = report["Report"]
        reportName = report['Name']
        packages = detailed_report["Dependencies"]
        for package in packages:
            packageName = package['Name']
            if packageName in pack_dict.keys():
                # add package usage info to list
                pack_dict[packageName]['Used In'].append(reportName)
                pack_dict[packageName]['Used In Count']+=1
            else:
                pack_dict[package['Name']]={'Version': package['Version'],
                                            'Used In Count':int(1),
                                            'Used In':[report['Name']],
                                            }
    return pack_dict

def generate_report(data,method_list):
    # TODO: could be good to add total node count
    sr_methods = search_deprecated_methods(data, method_list)
    sr_python_nodes = search_python_nodes(data),
    sr_code_blocks = search_code_blocks(data)
    sr_dependencies = search_dependencies(data)
    
    report = {
            'Name': data.get('Name',''),
            'Summary':{
                'Deprecated Node Count':len(sr_methods),
                'Python Node Count': len(sr_python_nodes),
                'Code Block Count': len(sr_code_blocks),
                'Dependency Count': len(sr_dependencies)
            },
            'Report': {
                'Deprecated Nodes': {'Node': list(set(sr_methods))},
                'Python Nodes': len(sr_python_nodes),
                'CodeBlockNodes': len(sr_code_blocks),
                'Dependencies': [{'Name': result[0], 'Version': result[1],'NodeCount':len(result[2]), 'Nodes': result[2]} for result in sr_dependencies],
            }
        }
    return report

def generate_report_summary(reports):
    
    deprecated_node_summary = {}
    python_node_summary = {}
    code_block_summary = {}
    dependency_summary = {}

    for report in reports:
        #report = r[next(iter(r))]
        rName = report["Name"]
        rSum = report["Summary"]
        dnc = rSum["Deprecated Node Count"]
        pnc = rSum["Python Node Count"]
        cnc = rSum["Code Block Count"]
        dc = rSum["Dependency Count"]
        
        if dnc > 0:
            deprecated_node_summary[rName] = dnc
        if pnc > 0:
            python_node_summary[rName] = pnc
        if cnc > 0:
            code_block_summary[rName] = cnc
        if dc > 0:
            dependency_summary[rName] = dc
    
    summary = {
                    "Files with Deprecated Nodes": {
                        "Count":len(deprecated_node_summary),
                        "Scripts":deprecated_node_summary
                    },
                    "Files with Python Nodes": {
                        "Count":len(python_node_summary),
                        "Scripts":python_node_summary
                    },
                    "Files with Code Blocks": {
                        "Count":len(code_block_summary),
                        "Scripts":code_block_summary
                    },
                    "Files with Dependencies": {
                        "Count":len(dependency_summary),
                        "Scripts":dependency_summary
                    },
                }
    return summary
        
"""def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        if isinstance(val, dict):
            child = dict_to_xml(key, val)
        elif isinstance(val, list):
            child = ET.SubElement(elem, key)
            for el in val:
                if isinstance(el, dict):
                    grandchild = dict_to_xml(key[:-1], el)  # Removes "s" from the key for individual elements
                    child.append(grandchild)
                else:
                    grandchild = ET.Element(key[:-1])  # Removes "s" from the key for individual elements
                    grandchild.text = el
                    child.append(grandchild)
        else:
            child = ET.Element(key)
            child.text = str(val)
        elem.append(child)
    return elem"""

def write_reports_to_json(reports, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reports, f, ensure_ascii=False, indent=4)

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

#--------------TEST FUNCTIONS----------------#
def testNewFunctions(testfile, deprecated_methods_file):
    
    deprecated_methods = read_deprecated_methods(deprecated_methods_file)
    testJson = read_json_file(testfile)

    pythonNodes = search_python_nodes(testJson)
    codeBlocks = search_code_blocks(testJson)
    dependencies = search_dependencies(testJson)

    output = generate_report(testJson,deprecated_methods)

    print("TEST COMPLETE")

def testmulti(path,deprecated_methods_file):
    deprecated_methods = read_deprecated_methods(deprecated_methods_file)
    file_list = find_files_with_extension(path,'.dyn')
    reports = {}
    print("{0} files found".format(len(file_list)))
    for file in file_list:
        data = read_json_file(file)
        r = generate_report(data, deprecated_methods)
        reports["Script: {0}".format(r.get('Name',''))] = r

    reports = [generate_report(read_json_file(file), deprecated_methods) for file in file_list]
    #filtered_output = list(filter(lambda x: x[-1] != [],output))
    #print("Update nodes in {0} files".format(len(filtered_output)))
    return reports

#--------------MAIN-------------------#
def main():
        #define CLI arguments
    parser = argparse.ArgumentParser(description='Analyze JSON files')
    
    parser.add_argument('deprecated_methods_file', help='File containing deprecated methods')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--directory', nargs='?', default=os.getcwd(),
                       const=os.getcwd(), help='Directory to analyze (default: current directory)')
    group.add_argument('-f', '--file', help='Single file to analyze')

    report_group = parser.add_argument_group('reports', 'types of reports to output')
    report_group.add_argument('-s', '--summary', action='store_true', help='Output summary report')
    report_group.add_argument('-a', '--detailed', action='store_true', help='Output detailed report')
    report_group.add_argument('-p', '--package', action='store_true', help='Output package summary')

    args = parser.parse_args()
    print("\n\nBEGIN\n\n")
    # At this point, args.directory will contain the directory passed by the user
    # or None if not provided. Similarly for args.file and args.methods
    deprecated_methods = read_deprecated_methods(args.deprecated_methods_file)
    if args.directory:
        # analyze all JSON files in the directory
        full_path = os.path.expanduser(args.directory)
        print(f'Analyzing directory: {full_path}')
        file_list = find_files_with_extension(full_path,'.dyn')
        print('-- Found {0} Files'.format(len(file_list)))
        reports = [generate_report(read_json_file(file), deprecated_methods) for file in file_list]
        print("-- SCAN COMPLETE --\n")

    elif args.file:
        # analyze single JSON file
        print(f'Analyzing file: {args.file}')
        reports = generate_report(read_json_file(args.file), deprecated_methods)
        print("-- SCAN COMPLETE --")

    output = {}

    if args.summary:
        output['Summary']= generate_report_summary(reports)
        print("- Summary report generated")
    if args.package:
        output['Package'] = generate_package_report(reports)
        print("- Package report generated")
    if args.detailed:
        output['Detailed'] = reports
        print("- Detailed report generated")

    write_reports_to_json(output, "DynamoNodeAnalysis.json")
    print ("\n\n-- Dynamo Library Scan Complete --\n\n")

if __name__ == "__main__":
    main()


"""Modes:
    1   detailed - print full report
    2   condensed - generate short report
        2.1     short report should just be the summary: Number of Deprecated nodes, Number of Python Nodes, Number of CodeBlocks. 
                filter out number of deprecated nodes = 0
    3   transposed - generate report by search
        3.1     deprecated nodes
        3.2     python engine
        3.3     code blocks
    4   severity - some combined metric with weight to estimate how much effort would have to go into updates
    you really want to be able to transpose this data, so you can see the scripts with deprecated nodes, python nodes, code blocks"""