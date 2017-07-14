import logging
#from google.appengine.api import memcache
import datetime
from datetime import date, timedelta
from django.conf import settings
from time import sleep
from django.conf import settings
import pyactiveresource
from pyactiveresource.activeresource import formats
from pyactiveresource.connection     import (
    Connection,
    ConnectionError,
    ServerError,
)
from django.core.cache import cache
from django.core.cache.backends.memcached import BaseMemcachedCache
import shopify

#import memcached
#client = memcache.Client([('127.0.0.1', 11211)])
#sample_obj = {"name": "Soliman",
#"lang": "Python"}
#client.set("sample_user", sample_obj, time=15)
#print ("Stored to memcached, will auto-expire after 15 seconds")
#print (client.get("sample_user"))

#import memcached_udp

#client = memcached_udp.Client([('192.168.0.1', 11211), ('192.168.0.5', 11211), ('127.0.0.1', 11211)])
#client = memcached_udp.Client([('127.0.0.1', 11211)])
#client.set('key1', 'value1')
#cache.set('key1', 'value1')
#r = client.get('key1')
#print ("Stored to memcached, will auto-expire after 15 seconds")
#print (cache.get("key1"))


# Store the response from the last request in the connection object
class ShopifyConnection(pyactiveresource.connection.Connection):
	response = None

	def __init__(self, site, user=None, password=None, timeout=None,
				format=formats.JSONFormat):
		super(ShopifyConnection, self).__init__(site, user, password, timeout, format)        

	def consume_token(uid, capacity, rate, min_interval):
		# Get this users last UID
		last_call_time = cache.get(uid+"_last_call_time")
		last_call_value = cache.get(uid+"_last_call_value")

		#print("the last call value")
		
		if last_call_time and last_call_value:
			# Calculate how many tokens are regenerated
			now = datetime.datetime.utcnow()
			delta = rate * ((now - last_call_time).seconds)

			# If there is no change in time then check what last call value was
			if delta == 0:
				tokensAvailable = min(capacity, capacity - last_call_value)
			# If there was a change in time, how much regen has occurred
			else:            
				tokensAvailable = min(capacity, (capacity - last_call_value) + delta)

			# No tokens available can't call
			if tokensAvailable <= min_interval:
				raise pyactiveresource.connection.ConnectionError(message="No tokens available for: " + str(uid))


	def _open(self, *args, **kwargs):
		uid = self.site.split("https://")[-1].split(".myshopify.com")[0]
		self.response = None
		retries = 0
		#print("the open motiv")
		while True:
			try:
				#self.consume_token(uid, 40, 2, 0.05)
				self.consume_token(uid, 40, 1.95, 0.05)
				self.response = super(ShopifyConnection, self)._open(*args, **kwargs)
				return self.response
				#
                # Set the memcache reference
				#cache.set_multi( {
				#	"_last_call_time": datetime.datetime.strptime(self.response.headers['date'], '%a, %d %b %Y %H:%M:%S %Z'), "_last_call_value": int(self.response.headers['x-shopify-shop-api-call-limit'].split('/',1)[0])}, 
				#				key_prefix=uid, time=25)
				#return self.response    
			#except (pyactiveresource.connection.ConnectionError, pyactiveresource.connection.ServerError) as err:
			except (ConnectionError, ServerError) as err:
				retries += 1
				if retries > settings.SHOPIFY_MAX_RETRIES:
					self.response = err.response
					logging.error("Logging error for _open ShopifyConnection: " + str(uid) + ":" + str(err.message))
					raise
				sleep(settings.SHOPIFY_RETRY_WAIT)
				
shopify.base.ShopifyConnection = ShopifyConnection				
