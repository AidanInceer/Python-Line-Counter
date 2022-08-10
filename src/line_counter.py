from counter import Counter
from args import get_arguments

direcorties_to_ignore = ['.git', '.next', 'node_modules', 'site-packages', '__pycache__']
types_to_ignore = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.svg']

def get_directory_to_scan(args):
    if args.directory is None:
        return input('\nDirectory path: ')

    return args.directory

def log(message):
    print(message)


if __name__ == '__main__':
    args = get_arguments()
    directory = get_directory_to_scan(args)
    counter = Counter(directory, args, direcorties_to_ignore, types_to_ignore)

    directories_count = counter.count_directories()
    log(f"Number of sub-directories to count {directories_count}")

    result = counter.count_lines()
    log(f"Number of lines found: {result}\n")

    input("Press enter to exit...")
