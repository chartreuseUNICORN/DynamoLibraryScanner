# Dynamo Library Scanner

This project is a command-line interface tool for analyzing JSON files generated from Dynamo, which is a visual programming tool. It can process a single file or a directory containing multiple files.

The main purpose of this tool is to identify usage of deprecated methods and provide an overview of package usage within a given set of scripts. This will help maintainers upgrade their scripts in a controlled manner.

## Usage

To use this tool, you need to provide the JSON file with elements to flag, the location of the JSON files to be analyzed, and the flags for reports. See the resources folder for a sample flagged components file

Here are the basic commands to run the script:

Analyze all JSON files in the current directory:
```
python DynamoLibraryScan.py deprecated_methods_file -d
```

Arguments:

- `deprecated_methods_file` : a JSON file describing flagged components to search for
- `-d`, `--directory` : directory to analyze. If no directory is specified, the current directory is used
- `-f`, `--file` : a single JSON file to analyze
- `-s`, `--summary` : output a summary report
- `-a`, `--detailed` : output a detailed report
- `-p`, `--package` : output a package summary
- `-c`, `--compressed` : output a compressed summary report as a CSV file

The reports are written to a JSON file in the same directory where the script was run, or the same directory as the file if `-f` is used.

For example, to generate a detailed and summary report for all files in a directory, use the following command:

```
python DynamoLibraryScan.py deprecated_methods_file -d directory -s -a
```

Remember to replace `directory`, `file`, and `deprecated_methods_file` with your actual paths.

## License

[MIT](https://choosealicense.com/licenses/mit/)
