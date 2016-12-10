import json
import urllib.request, urllib.error, urllib.parse
import codecs
import logging

logger = logging.getLogger(__name__)

class HTTP(object):

    @staticmethod
    def load_url(url, data = None, headers = {}, method = None):
        encoded_data = None
        if data:
            encoded_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, encoded_data, headers, method = method)
        response = urllib.request.urlopen(req)
        reader = codecs.getreader("utf-8")
        return reader(response)

    @staticmethod
    def load_urls(url, data = None, headers = {}, method = None):
        return HTTP.load_url(url, data, headers, method).read()

    @staticmethod
    def load_json(url, data = None, headers = {}, method = None):
        try:
            return json.load(HTTP.load_url(url, data, headers, method))
        except ValueError as e:
            logger.exception("Cannot decode json from '%s'", url)
            return None
