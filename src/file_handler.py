import json


class SimpleEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__()


def write_to_file(data):
    with open('data.json', 'w') as data_file:
        data_file.write(to_json(data))

    with open('data.js', 'w') as data_file:
        data_file.write('const DATA = ' + to_json(data))


def to_json(data):
    return json.dumps(data, indent=4, cls=SimpleEncoder)