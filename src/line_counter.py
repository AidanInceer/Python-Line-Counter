import argparse
from os import listdir, walk
from os.path import isfile, isdir, join

# from print_progress import print_progress_bar

direcorties_to_ignore = ['.git', '.next', 'node_modules', 'site-packages', '__pycache__']
types_to_ignore = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.svg']


def count_directories(path, args):
    count = 0
    for _, dirs, _ in walk(path):
        if not args.all:
            dirs[:] = [d for d in dirs if d not in direcorties_to_ignore]
        for _ in dirs:
                count += 1
    return count


def item_line_count(path, args, depth = 0, total = 0, iteration = 0):
    skip = False
    
    if depth > args.maxdepth and args.maxdepth > 0:
        return 0

    if isdir(path):

        iteration += 1

        # if total > 0:
            # print_progress_bar(iteration, total)

        for ignore in direcorties_to_ignore:
            if ignore in path and not args.all:
                skip = True 

        if skip:
            return 0

        if args.printdirectory: print(path)
        return dir_line_count(path, args, depth + 1, total, iteration)

    elif isfile(path):
        if args.printfile: 
            print(path)
        if path.lower().endswith(tuple(types_to_ignore)): 
            return 0
        return len(open(path, 'rb').readlines())

    return 0


def dir_line_count(dir, args, depth = 0, total = 0, iteration = 0):
    return sum(map(lambda item: item_line_count(join(dir, item), args, depth + 1, total, iteration), listdir(dir)))


def add_arguments(parser):
    parser.add_argument("-m", "--maxdepth", help="Sets the max recusrion depth", type=int, default=-1)
    parser.add_argument("-d", "--directory", help="The directory to scan", type=str)
    parser.add_argument("-pf", "--printfile", help="Prints the path of every file", action="store_true")
    parser.add_argument("-pd", "--printdirectory", help="Prints the path of every directory", action="store_true")
    parser.add_argument("-a", "--all", help="Scans all directories, even those in the ingore list", action="store_true")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()
    args.git = True

    if args.directory is None:
        directory = input('\nDirectory path: ')
    else:
        directory = args.directory

    directories_count = count_directories(directory, args)
    print(f"Number of sub-directories to count {directories_count}")
    
    result = dir_line_count(directory, args, total = directories_count)
    print(f"Number of lines found: {result}\n")

    input("Press enter to exit")
