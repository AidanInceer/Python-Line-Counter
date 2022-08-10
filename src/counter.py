from os import listdir, walk
from os.path import isfile, isdir, join

class Counter:

    def __init__(self, path, args, ignored_directories=[], ignored_types=[]):
        self.path = path
        self.args = args
        self.ignored_directories = ignored_directories
        self.ignored_types = ignored_types


    def count_directories(self):
        count = 0
        for _, dirs, _ in walk(self.path):
            if not self.args.all:
                dirs[:] = [d for d in dirs if d not in self.ignored_directories]
            for _ in dirs:
                    count += 1
        return count 


    def count_lines(self):
        return self._directory_line_count(self.path)


    def count_lines_in_file(self, path):
        if self.args.printfile: print(path)

        if path.lower().endswith(tuple(self.ignored_types)): 
            return 0

        return len(open(path, 'rb').readlines())


    def _directory_line_count(self, dir, depth = 0, total = 0, iteration = 0):
        return sum(
                map(lambda item: self._count_lines_in_item(join(dir, item), depth + 1, total, iteration), 
                    listdir(dir)
                )
            )


    def _count_lines_in_item(self, path, depth = 0, total = 0, iteration = 0):
        if depth > self.args.maxdepth and self.args.maxdepth > 0:
            return 0

        if isdir(path):
            return self._count_lines_in_driectory(path, depth, total, iteration)
            

        elif isfile(path):
            return self.count_lines_in_file(path)

        return 0


    def _count_lines_in_driectory(self, path, depth, total, iteration):
        iteration += 1

        for ignore in self.ignored_directories:
            if ignore in path and not self.args.all:
                return 0

        if self.args.printdirectory: print(path)

        return self._directory_line_count(path, depth + 1, total, iteration)

    