
import os
import json

class JSONConfigLoader():
    def __init__(self, base_path):
        self.sources = [
            os.path.dirname(os.getcwd()),
            os.path.dirname(os.path.abspath(base_path)),
            os.path.expanduser('~'),
            '/etc',
        ]

    def load(self, filename):
        tries = []
        for source in self.sources:
            file_path = os.path.join(source, filename)
            tries.append(file_path)
            if not os.path.exists(file_path):
                continue
            with open(file_path) as f:
                return json.load(f)

        raise Exception("Config file not found in: %s" % tries)