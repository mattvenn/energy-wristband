import mechanize
import json
import threading

class Xively_Exception(Exception):
    def __init__(self, message):
        super(Xively_Exception, self).__init__(message)
        self.message = message

class xively(threading.Thread):

    url_base = "http://api.xively.com/v2/feeds/"
    version = '1.0.0'

    def __init__(self, feed_id, logging, keyfile="xively.key", timeout=5, uptime=False):
        threading.Thread.__init__(self)

        # private key stored in a file
        try:
            api_key = open(keyfile).readlines()[0].strip()
        except IOError as e:
            raise Xively_Exception("missing api key file: xively.key")

        self.feed_id = feed_id
        self.timeout = timeout
        self.logger = logging.getLogger('xively')

        self.opener = mechanize.build_opener()
        self.opener.addheaders = [('X-ApiKey', api_key)]
        self.data = []
        self.payload = {}

        if uptime:
            self.add_uptime()

    def add_uptime(self):
        f=open("/proc/uptime","r");
        uptime_string=f.readline()
        f.close()
        uptime=uptime_string.split()[0]
        self.add_datapoint('uptime', uptime)

    def add_datapoint(self, dp_id, dp_value):
        self.data.append({'id': dp_id, 'current_value': dp_value})

    def run(self):
        self.payload['version'] = xively.version
        self.payload['id'] = self.feed_id
        self.payload['datastreams'] = self.data
        url = self.url_base + self.feed_id + "?_method=put"

        try:
            self.opener.open(url, json.dumps(self.payload),
                             timeout=self.timeout)
            self.logger.info("sent")
        except mechanize.HTTPError as e:
            self.logger.warning("HTTP error: %s" % e)
        except mechanize.URLError as e:
            self.logger.warning("URL error: %s" % e)


if __name__ == '__main__':
    feed_id = "130883"
    xively_timeout = 10
    import logging
    logging.basicConfig(level=logging.INFO)
    xively_t = xively(feed_id, logging, timeout=xively_timeout, uptime=True)
    xively_t.start()
