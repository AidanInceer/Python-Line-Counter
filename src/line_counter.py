import configparser
import os

from counter import Counter
from args import get_arguments
from tree import print_tree

def get_config():
    config = configparser.ConfigParser()
    config.read(config.read(os.path.join(os.path.dirname(__file__), 'config.ini')))
    directories_to_ignore = config.get('MAIN', 'directories_to_ignore').replace(" ", "").split(',')
    types_to_ignore = config.get('MAIN', 'types_to_ignore').replace(" ", "").split(',')
    return directories_to_ignore, types_to_ignore


def get_directory_to_scan(args):
    if args.directory is None:
        return input('\nDirectory path: ')

    return args.directory


def log(message):
    print(message)


if __name__ == '__main__':
    args = get_arguments()

    directories_to_ignore, types_to_ignore = get_config()

    directory = get_directory_to_scan(args)
    counter = Counter(directory, args, directories_to_ignore, types_to_ignore)

    directories_count = counter.count_directories()
    log(f"Number of sub-directories to count {directories_count}")

    result = counter.count_lines()
    log(f"Number of lines found: {result}\n")

    # print_tree(counter.data)
    input("Press enter to exit...")
