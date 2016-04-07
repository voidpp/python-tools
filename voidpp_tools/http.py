import json
import urllib.request, urllib.error, urllib.parse

class HTTP(object):

    @staticmethod
    def load_url(url, data = None, headers = {}):
        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req)
        return response

    @staticmethod
    def load_urls(url, data = None, headers = {}):
        return HTTP.load_url(url, data, headers).read()

    @staticmethod
    def load_json(url, data = None, headers = {}):
        try:
            return json.load(HTTP.load_url(url, data, headers))
        except ValueError:
            return None
