from enum import Enum
import json
from os import listdir, walk
from os.path import isfile, isdir, join

from tree import make_tree

class Counter:

    def __init__(self, path, args, ignored_directories=[], ignored_types=[]):
        self.path = path
        self.args = args
        self.ignored_directories = ignored_directories
        self.ignored_types = ignored_types
        self.data = {}


    def count_directories(self):
        count = 0
        for _, dirs, _ in walk(self.path):
            if not self.args.all:
                dirs[:] = [d for d in dirs if d not in self.ignored_directories]
            for _ in dirs:
                count += 1
        return count 


    def count_lines(self):
        line_count = self._directory_line_count(self.path)
        
        if self.args.save: 
            self.data['line_count'] = line_count
            self.data['root'] = self.path

            print('Saving to file...')
            make_tree(self.path, self.data)
            write_to_file(self.data)

        return line_count


    def count_lines_in_file(self, path):
        if path.lower().endswith(tuple(self.ignored_types)): 
            return 0

        line_count = len(open(path, 'rb').readlines())

        if self.args.save: self.data[path] = Item(path, ItemType.FILE, line_count)


        return line_count


    def _directory_line_count(self, dir, depth = 0, total = 0, iteration = 0):
        line_count =  sum(
                map(lambda item: self._count_lines_in_item(join(dir, item), depth + 1, total, iteration), 
                    listdir(dir)
                )
            )

        if self.args.printdirectory: print(dir)
        if self.args.save: self.data[dir] = Item(dir, ItemType.DIR, line_count)

        return line_count


    def _count_lines_in_item(self, path, depth = 0, total = 0, iteration = 0):
        if depth > self.args.maxdepth and self.args.maxdepth > 0:
            return 0

        if isdir(path):
            return self._count_lines_in_driectory(path, depth, total, iteration)
            

        elif isfile(path):
            if self.args.printfile: print(path)
            return self.count_lines_in_file(path)

        return 0


    def _count_lines_in_driectory(self, path, depth, total, iteration):
        iteration += 1

        for ignore in self.ignored_directories:
            if ignore in path and not self.args.all:
                return 0

        if self.args.printdirectory: print(path)

        return self._directory_line_count(path, depth + 1, total, iteration)


class ItemType(Enum):
    FILE = 1
    DIR = 2
    OTHER = 3

class Item:
    def __init__(self, path: str, type : ItemType, lines : int):
        self.path = path
        self.type = type
        self.lines = lines
        self.children = []

    def __dict__(self):
        return {'path': self.path, 'type': self.type.name, 'lines': self.lines, 'children': self.children}

    def __repr__(self):
        return f'<counter.Item path:{self.path}, type: {self.type.name}, lines: {self.lines},  children: {self.children}'


class SimpleEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__()


def write_to_file(data):
    with open('data.json', 'w') as data_file:
        data_file.write(to_json(data))

    with open('data.js', 'w') as data_file:
        data_file.write('const data = ' + to_json(data))


def to_json(data):
    return json.dumps(data, indent=4, cls=SimpleEncoder)