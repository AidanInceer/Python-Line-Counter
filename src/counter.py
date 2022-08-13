from argparse import ArgumentParser
from enum import Enum
from os import listdir, walk
from os.path import isfile, isdir, join

from config import Config
from file_handler import write_to_file
from tree import print_tree, make_tree

class Counter:
    path: str 
    args: ArgumentParser
    config: Config
    data: dict

    def __init__(self, path:str, args:ArgumentParser, config:Config):
        self.path = path
        self.args = args
        self.config = config
        self.data = {}

    
    def print_tree(self):
        if len(self.data.keys()) == 0:
            print('Tree is empty...')
        elif 'root' not in self.data:
            print('Tree has no root...')
        else:
            print_tree(self.data)


    def count_directories(self) -> int:
        count = 0
        for _, dirs, _ in walk(self.path):
            if not self.args.all:
                dirs[:] = [d for d in dirs if d not in self.config.directories_to_ignore]
            count += len(dirs)
        return count 


    def count_lines(self) -> int:
        line_count = self._count_lines_in_directory(self.path)
        
        if self.args.save: 
           self._save_result(line_count)

        return line_count


    def _save_result(self, line_count):
        self.data['line_count'] = line_count
        self.data['root'] = self.path

        print('Saving to file...')
        make_tree(self.path, self.data)
        write_to_file(self.data)


    def count_lines_in_file(self, path:str) -> int:
        if path.lower().endswith(tuple(self.config.types_to_ignore)): 
            return 0

        line_count = len(open(path, 'rb').readlines())

        if self.args.save: self.data[path] = Item(path, ItemType.FILE, line_count)

        return line_count


    def _count_lines_in_directory(self, dir:str, depth:int = 0, total:int = 0, iteration:int = 0) -> int:
        line_count =  sum(
                map(lambda item: self._count_lines_in_item(join(dir, item), depth + 1, total, iteration), 
                    listdir(dir)
                )
            )

        if self.args.printdirectory: print(dir)
        if self.args.save: self.data[dir] = Item(dir, ItemType.DIR, line_count)

        return line_count


    def _count_lines_in_item(self, path:str, depth:int = 0, total:int = 0, iteration:int = 0) -> int:
        if depth > self.args.maxdepth and self.args.maxdepth > 0:
            return 0

        if isdir(path):
            return self._count_lines_in_driectory(path, depth, total, iteration)
            
        elif isfile(path):
            if self.args.printfile: print(path)
            return self.count_lines_in_file(path)

        return 0


    def _count_lines_in_driectory(self, path:str, depth:int, total:int, iteration:int) -> int:
        iteration += 1

        for ignore in self.config.directories_to_ignore:
            if ignore in path and not self.args.all:
                return 0

        if self.args.printdirectory: print(path)

        return self._count_lines_in_directory(path, depth + 1, total, iteration)


class ItemType(Enum):
    FILE = 1
    DIR = 2
    OTHER = 3

class Item:
    def __init__(self, path: str, type:ItemType, lines:int):
        self.path = path
        self.type = type
        self.lines = lines
        self.children = []

    def __dict__(self):
        return {'path': self.path, 'type': self.type.name, 'lines': self.lines, 'children': self.children}

    def __repr__(self):
        return f'<counter.Item path:{self.path}, type: {self.type.name}, lines: {self.lines},  children: {self.children}'
