from os import walk

def make_tree(path, data):
    for path, dirnames, filenames in walk(path):
        if (path in data):
            currNode = Node(path, dirnames, filenames, data)
            data[path].children = currNode.children

class Node(object):
    def __init__(self, path, child_dirs, child_files, data):
        self.path = path
        self.child_dirs = list(map(lambda dir : path + '\\' + dir, child_dirs))
        self.child_files = list(map(lambda dir : path + '\\' + dir, child_files))
        
        self.children = self.child_dirs + self.child_files
        
        if (path in data):
            self.data = data[path]


def print_tree(data, root = None, indent = 0):

    if root == None:
        root = data['root']

    if root not in data:
        return
    
    node = data[root]
    
    print(f"{'|  ' * indent}{node.lines} - {node.path}")

    for child in node.children:
        print_tree(data, child, indent + 1)
