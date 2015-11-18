import json
import urllib2

class HTTP(object):

    @staticmethod
    def load_url(url, data = None, headers = {}):
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
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
