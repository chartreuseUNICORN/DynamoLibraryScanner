# Dynamo Node Analysis

This project is a command-line interface tool for analyzing JSON files generated from Dynamo, which is a visual programming tool. It can process a single file or a directory containing multiple files.

The main purpose of this tool is to identify usage of deprecated methods and provide an overview of package usage within a given set of scripts. This will help maintainers upgrade their scripts in a controlled manner.

## Installation

Clone this repository to your local machine.

## Usage

To use this tool, you need to provide it with the location of the JSON files to be analyzed, and a list of deprecated methods. The list of deprecated methods should be in a plain text file, with one method per line.

`python main.py -d directory deprecated_methods_file`
`python main.py -f file deprecated_methods_file`

-d, --directory - analyze all JSON files in the specified directory
-f, --file - analyze a single JSON file
deprecated_methods_file - a file listing the deprecated methods to search for

Additionally, you can specify what type of reports to generate:

`python main.py -d directory deprecated_methods_file -s`
`python main.py -d directory deprecated_methods_file -a`
`python main.py -d directory deprecated_methods_file -p`

-s, --summary - output a summary report
-a, --detailed - output a detailed report
-p, --package - output a package summary

The reports are written to a JSON file in the current directory.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

Remember to replace `directory`, `file`, and `deprecated_methods_file` with your actual paths.
