import mechanize
import json
import time
import threading

class xively(threading.Thread):

    url_base = "http://api.pachube.com/v2/feeds/"
    version = '1.0.0'

    def __init__(self, feed_id, logging, keyfile="api.key"):
        threading.Thread.__init__(self)
        #private key stored in a file
        keyfile="api.key"
        api_key = open(keyfile).readlines()[0].strip()
        self.feed_id = feed_id
        self.opener = mechanize.build_opener()
        self.opener.addheaders = [('X-ApiKey',api_key)]
        self.data = []
        self.payload = {}
        self.logger = logging.getLogger('xively')

    def add_datapoint(self,dp_id,dp_value):
        self.data.append({'id':dp_id, 'current_value':dp_value})

    def run(self):
        self.payload['version'] = xively.version
        self.payload['id'] = self.feed_id
        self.payload['datastreams'] = self.data
        url = self.url_base + self.feed_id + "?_method=put"
        try:
            self.opener.open(url,json.dumps(self.payload),timeout=5)
        except mechanize.HTTPError as e:
            self.logger.error("An HTTP error occurred: %s " % e)
        except mechanize.URLError as e:        
            self.logger.error("A URL error occurred: %s " % e)
        self.logger.info("sent")
