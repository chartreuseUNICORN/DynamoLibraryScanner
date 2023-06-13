import FileUtils

def deprecated_methods( data):
    searchResult = []
    name = data.get('Name','')
    nodes = data.get('Nodes', [])
    for node in nodes:
        function_signature = node.get('FunctionSignature', '')
        node_type = node.get('NodeType','')
        if node_type == 'FunctionNode':
                searchResult.append(function_signature) 
    # does this need to return all nodes, or all unique nodes
    return list(set(searchResult))

def python_nodes (data):
    searchResult = []
    nodes = data.get('Nodes',[])
    for node in nodes:
        node_type = node.get('NodeType','')
        if node_type == 'PythonScriptNode':
            engine = node.get('Engine','')
            if engine == 'IronPython2':
                searchResult.append(node_type)
    return searchResult

def code_blocks (data):
    searchResult = []
    nodes = data.get('Nodes',[])
    for node in nodes:
        node_type = node.get('NodeType','')
        if node_type == 'CodeBlockNode':
            searchResult.append(node_type)
    return searchResult

def dependencies (data):
    searchResult = []
    deps = data.get('NodeLibraryDependencies',[])
    node_lookup = build_node_map(data.get('Nodes',[]))
    for d in deps:
        dType = d.get('ReferenceType','')
        if dType == "Package":    
            package_nodes = [node_lookup.get(id) for id in d.get('Nodes',[])]
            searchResult.append((d.get('Name',''),d.get('Version',''),package_nodes))
    return searchResult

def build_node_map (nodes):
    node_map = {node.get('Id', ''): node.get('FunctionSignature', '') for node in nodes}
    return node_map

def file_methods (json_file, deprecated_methods):    
    data = FileUtils.read_json_file(json_file)
    name = data.get('Name','')
    searchResults = deprecated_methods(data, deprecated_methods)
    #print("Result: {0}".format(searchResults))
    return (name,list(set(searchResults)))