import configparser
import os

class Config:

    filename: str
    config_parser: configparser
    directories_to_ignore: list[str]
    types_to_ignore: list[str]

    def __init__(self, filename : str):
        self.filename = filename
        self.config_parser = configparser.ConfigParser()
    

    def read_config(self):
        self.config_parser.read(self.config_parser.read(os.path.join(os.path.dirname(__file__), self.filename)))

        self.directories_to_ignore = self._get_list('directories_to_ignore')
        self.types_to_ignore = self._get_list('types_to_ignore')


    def _get_list(self, item : str) -> list[str]:
        return self.config_parser.get('MAIN', item).replace(" ", "").split(',')


def get_config(filename : str) -> Config:
    config = Config(filename)
    config.read_config()
    return config
    