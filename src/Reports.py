import Search
import json

def generate_report(data,flags):
    # TODO: could be good to add total node count
    #   1 i feel like  these searches could be combined in some way
    #   2 want to include flagged lists for each metric (nodes, python nodes, code blocks, dependencies)
    #   3 make flags optional in report generation, searches (what's the best way to do this, polymorphism? pass an empty argument?)

    fNodes = flags.get('FlaggedNodes','')
    fPackages = flags.get('FlaggedPackages','')

    sr_methods = Search.deprecated_methods(data)
    sr_python_nodes = Search.python_nodes(data)
    sr_code_blocks = Search.code_blocks(data)
    sr_dependencies = Search.dependencies(data)

    flagged_Nodes = list(set(sr_methods) & set(fNodes))
    flagged_Packages = [i[0] for i in sr_dependencies if i[0] in fPackages]
    
    # so what does this want to be:
    # Nodes/Flagged Nodes
    # PythonNodeCount / Flagged Python Nodes
    # CodeBlockCount / Flagged Code Blocks
    # DependencyCount / Flagged Dependency Count
    if len(flagged_Packages) > len(fPackages):
        print("hold up")

    report = {
            'Name': data.get('Name',''),
            'Summary':{
                'Unique Node Count': len(sr_methods),
                'Flagged Node Count':len(flagged_Nodes),
                'Python Node Count': len(sr_python_nodes),
                'Code Block Count': len(sr_code_blocks),
                'Dependency Count': len(sr_dependencies),
                'Flagged Dependency Count': len(list(set(flagged_Packages)))
            },
            'Report': {
                'Deprecated Nodes': {'Node': list(set(flagged_Nodes))},
                'Python Nodes': len(sr_python_nodes),
                'CodeBlockNodes': len(sr_code_blocks),
                'Dependencies': [{'Name': result[0], 'Version': result[1],'NodeCount':len(result[2]), 'Nodes': result[2]} for result in sr_dependencies],
            }
        }
    return report

def report_package_usage (data):
    depends = data.get('NodeLibraryDependencies','')
    packages = list(filter(lambda x: x.ReferenceType == 'Package',depends))
    report = [(package.Name,package.Version,len(package.Nodes)) for package in packages]
    return report

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

def generate_report_compressed(reports):
    compressed = [['Name','Flagged Nodes','Python Nodes','Code Blocks','Dependencies',"Flagged Dependencies"]]
    for report in reports:
        summary = report['Summary']
        compressed.append([
                            report['Name'],
                            summary['Flagged Node Count'],
                            summary['Python Node Count'],
                            summary['Code Block Count'],
                            summary['Dependency Count'],
                            summary['Flagged Dependency Count']
                            ]
                        )

    return compressed

def generate_report_summary(reports):
    
    deprecated_node_summary = {}
    python_node_summary = {}
    code_block_summary = {}
    dependency_summary = {}
    fdependency_summary = {}
    #TODO: condense these repeated patterns
    for report in reports:
        #report = r[next(iter(r))]
        rName = report["Name"]
        rSum = report["Summary"]
        dnc = rSum["Flagged Node Count"]
        pnc = rSum["Python Node Count"]
        cnc = rSum["Code Block Count"]
        dc = rSum["Dependency Count"]
        fdc = rSum['Flagged Dependency Count']
        
        if dnc > 0:
            deprecated_node_summary[rName] = dnc
        if pnc > 0:
            python_node_summary[rName] = pnc
        if cnc > 0:
            code_block_summary[rName] = cnc
        if dc > 0:
            dependency_summary[rName] = dc
        if fdc > 0:
            fdependency_summary[rName] = fdc
    
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
                    "Flagged Dependencies": {
                        "Count": len(fdependency_summary),
                        "Scripts": fdependency_summary
                    }
                }
    return summary

def write_reports_to_json(reports, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reports, f, ensure_ascii=False, indent=4)