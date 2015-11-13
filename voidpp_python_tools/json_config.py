
import os
import json

class JSONConfigLoader():
    def __init__(self):
        self.sources = [
            os.path.dirname(os.getcwd()),
            os.path.dirname(os.path.abspath(__file__)),
            os.path.expanduser('~'),
            '/etc',
        ]

    def load(self, filename):
        for source in self.sources:
            file_path = os.path.join(source, filename)
            if not os.path.exists(file_path):
                continue
            with open(file_path) as f:
                return json.load(f)

        return None
