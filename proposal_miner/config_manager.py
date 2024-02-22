import configparser
import os
from collections.abc import MutableMapping


class Config(MutableMapping):
    _instance = None
    config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def read(self, path: str):
        if self.config is None:
            self.config = configparser.ConfigParser()
        if not os.path.exists(path):
            raise FileNotFoundError(f'The config INI file {path} does not exist!')
        self.config.read(path)

    def __getitem__(self, item: str) -> configparser.SectionProxy:
        return self.config.__getitem__(item)

    def __setitem__(self, *args, **kwargs):
        return self.config.__setitem__(*args, **kwargs)

    def __delitem__(self, key: str):
        return self.config.__delitem__(key)

    def __iter__(self):
        return self.config.__iter__()

    def __len__(self) -> int:
        return self.config.__len__()
