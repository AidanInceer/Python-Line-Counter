from counter import Counter
from args import get_arguments
from config import get_config
# from tree import print_tree

def get_directory_to_scan(args):
    if args.directory is None:
        return input('\nDirectory path: ')

    return args.directory


def log(message):
    print(message)


if __name__ == '__main__':
    args = get_arguments()

    directory = get_directory_to_scan(args)
    counter = Counter(directory, args, get_config('config.ini'))

    directories_count = counter.count_directories()
    log(f"Number of sub-directories to count {directories_count}")

    result = counter.count_lines()
    log(f"Number of lines found: {result}\n")

    # print_tree(counter.data)
    input("Press enter to exit...")
