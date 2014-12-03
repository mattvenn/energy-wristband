#!/usr/bin/python

# This code is released into the public domain (though I'd be interested in seeing
#  improvements or extensions, if you're willing to share back).

import mechanize
import json
import time
import threading

class CosmFeedUpdate(threading.Thread):

  _url_base = "http://api.pachube.com/v2/feeds/"
  _feed_id = None
  _version = None
  ## the substance of our update - list of dictionaries with keys 'id' and 'current_value'
  _data = None
  ## the actual object we'll JSONify and send to the API endpoint
  _payload = None
  _opener = None

  def __init__(self, feed_id, apikey,logging):
    threading.Thread.__init__(self)
    self._version = "1.0.0"
    self._feed_id = feed_id
    self._opener = mechanize.build_opener()
    self._opener.addheaders = [('X-ApiKey',apikey)]
    self._data = []
    self._payload = {}
    self.logger = logging.getLogger('xively')

  def addDatapoint(self,dp_id,dp_value):
    self._data.append({'id':dp_id, 'current_value':dp_value})

  def buildUpdate(self):
    self._payload['version'] = self._version
    self._payload['id'] = self._feed_id
    self._payload['datastreams'] = self._data

  def run(self):
    url = self._url_base + self._feed_id + "?_method=put"
    try:
      self._opener.open(url,json.dumps(self._payload),timeout=5)
    except mechanize.HTTPError as e:
      self.logger.error("An HTTP error occurred: %s " % e)
    except mechanize.URLError as e:    
      self.logger.error("A URL error occurred: %s " % e)
    self.logger.info("sent")
