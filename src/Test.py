import Search
import Reports
import FileUtils

def testNewFunctions(testfile, deprecated_methods_file):
    
    deprecated_methods = FileUtils.read_json_file(deprecated_methods_file)
    testJson = FileUtils.read_json_file(testfile)

    pythonNodes = Search.python_nodes(testJson)
    codeBlocks = Search.code_blocks(testJson)
    dependencies = Search.dependencies(testJson)

    output = Reports.generate_report(testJson,deprecated_methods)

    print("TEST COMPLETE")

def testmulti(path,deprecated_methods_file):
    deprecated_methods = FileUtils.read_json_file(deprecated_methods_file)
    file_list = FileUtils.find_files_with_extension(path,'.dyn')
    reports = {}
    print("{0} files found".format(len(file_list)))
    for file in file_list:
        data = FileUtils.read_json_file(file)
        r = Reports.generate_report(data, deprecated_methods)
        reports["Script: {0}".format(r.get('Name',''))] = r
    # apparently VERY OLD dynamo files are saved as xml format, not JSON
    # 
    reports = [Reports.generate_report(FileUtils.read_json_file(file), deprecated_methods) for file in file_list]
    #filtered_output = list(filter(lambda x: x[-1] != [],output))
    #print("Update nodes in {0} files".format(len(filtered_output)))
    return reports