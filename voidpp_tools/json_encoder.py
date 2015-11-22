
import json

class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__()
