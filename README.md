# Python-line-counter

Counts the number of lines in files in a directory.

## About

This is a simple Python script which, given a directory, will print the total number of lines in every file.

## Installation

Download the src folder.

## Usage

Run line_counter.py with the following optional commands:

```-h, --help              show this help message and exit
-m MAXDEPTH, --maxdepth MAXDEPTH    Sets the max recusrion depth
-d DIRECTORY, --directory DIRECTORY The directory to scan
-pf, --printfile        Prints the path of every file
pd, --printdirectory    Prints the path of every directory
-a, --all               Scans all directories, even those in the ingore list
-s, --save            Save results to file
```

### Ignore list

By default, these directories will be ignored:
.git,.next, node_modules, site-packages, \_\_pycache\_\_

and these file types will be ignored:
.png, .jpg, .jpeg, .tiff, .bmp, .gif, .svg
