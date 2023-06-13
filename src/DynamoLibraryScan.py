import os
import csv
import xml.etree.ElementTree as ET
import argparse
import FileUtils
import Reports
#import tabulate

def main():
    # define CLI arguments
    parser = argparse.ArgumentParser(description='Analyze JSON files')
    #TODO: update these variable names, add try/catch to enable run without flag definitions
    parser.add_argument('deprecated_methods_file', help='File containing deprecated methods')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--directory', nargs='?', default=os.getcwd(),
                       const=os.getcwd(), help='Directory to analyze (default: current directory)')
    group.add_argument('-f', '--file', help='Single file to analyze')

    report_group = parser.add_argument_group('reports', 'types of reports to output')
    report_group.add_argument('-s', '--summary', action='store_true', help='Output summary report')
    report_group.add_argument('-a', '--detailed', action='store_true', help='Output detailed report')
    report_group.add_argument('-p', '--package', action='store_true', help='Output package summary')
    report_group.add_argument('-c', '--compressed', action='store_true', help='Output package summary')

    args = parser.parse_args()
    print("\n-- Begin Library Scan--\n")
    flags = FileUtils.read_json_file(args.deprecated_methods_file)

    output_directory = ''
    reports = []

    if args.directory:
        full_path = os.path.expanduser(args.directory)
        print(f'Analyzing directory: {full_path}')
        file_list = FileUtils.find_files_with_extension(full_path,'.dyn')
        print('-- Found {0} Files'.format(len(file_list)))
        #valid_file_list = [file for file in file_list if is_valid_json(file)]
        valid_file_list = file_list
        print("-- Found {0} invalid Files".format((len(file_list)-len(valid_file_list))))
        if len(valid_file_list) != len(file_list):
            user_input = input("\n> Display Invalid Files? (y/n);")
            if user_input.lower() == 'y':
                [print(filename) for filename in set(file_list).difference(set(valid_file_list))]

        reports = [Reports.generate_report(FileUtils.read_json_file(file), flags) for file in valid_file_list]

        print("-- SCAN COMPLETE --\n")
        output_directory = full_path

    elif args.file:
        print(f'Analyzing file: {args.file}')
        reports = Reports.generate_report(FileUtils.read_json_file(args.file), flags)
        print("-- SCAN COMPLETE --")
        output_directory = os.path.dirname(os.path.expanduser(args.file))

    output = {}

    if args.summary:
        output['Summary'] = Reports.generate_report_summary(reports)
        print("- Summary report generated")
    if args.package:
        output['Package'] = Reports.generate_package_report(reports)
        print("- Package report generated")
    if args.detailed:
        output['Detailed'] = reports
        print("- Detailed report generated")
    if args.compressed:
        compressed = Reports.generate_report_compressed(reports)
        print("- Compressed report generated")
        """user_input = input("\nDisplay Compressed Summary? (y/n):")
        
        if user_input.lower() == 'y':
                print(tabulate(compressed, headers = 'firstrow', tablefmt = 'fance_grid'))"""

        with open(os.path.join(output_directory, 'DynamoNodeAnalysis_Compressed.csv'), 'w', newline = '') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(compressed)

    Reports.write_reports_to_json(output, os.path.join(output_directory, "DynamoNodeAnalysis.json"))
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