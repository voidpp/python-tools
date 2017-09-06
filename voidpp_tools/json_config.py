
import json

from .json_encoder import JsonEncoder
from .config_loader import ConfigLoader, ConfigFormatter

class JSONConfigFormatter(ConfigFormatter):

    def __init__(self, encoder, indent = None):
        self._encoder = encoder
        self._indent = indent

    def encode(self, data):
        return json.dumps(data, indent =  self._indent, cls = self._encoder)

    def decode(self, data):
        return json.loads(data)

# this is a backward compatibility class, because the loader refactored to a format independent ConfigLoader class
class JSONConfigLoader(ConfigLoader):
    def __init__(self, base_path, encoder = JsonEncoder, nested = False):
        super(JSONConfigLoader, self).__init__(JSONConfigFormatter(encoder), base_path, nested)
