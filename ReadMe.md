# Dynamo Node Analysis

This project is a command-line interface tool for analyzing JSON files generated from Dynamo, which is a visual programming tool. It can process a single file or a directory containing multiple files.

The main purpose of this tool is to identify usage of deprecated methods and provide an overview of package usage within a given set of scripts. This will help maintainers upgrade their scripts in a controlled manner.

## Installation

Clone this repository to your local machine using the following command in your terminal:

```
git clone https://github.com/your-repo/dynamo-node-analysis.git
```

Once cloned, navigate into the project's directory:

```
cd dynamo-node-analysis
```

## Usage

To use this tool, you need to provide it with the location of the JSON files to be analyzed and a list of deprecated methods. The list of deprecated methods should be in a plain text file, with one method per line.

Here are the basic commands to run the script:

Analyze all JSON files in the current directory:
```
python main.py deprecated_methods_file -d
```

Analyze all JSON files in a specified directory:
```
python main.py deprecated_methods_file -d directory
```

Analyze a single JSON file:
```
python main.py deprecated_methods_file -f file
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
python main.py deprecated_methods_file -d directory -s -a
```

Remember to replace `directory`, `file`, and `deprecated_methods_file` with your actual paths.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

---
