from time import sleep
from django.conf import settings
from pyactiveresource.activeresource import formats
from pyactiveresource.connection     import (
    Connection,
    ConnectionError,
    ServerError,
)
import shopify


class ShopifyConnection(Connection, object):
	response = None

	def __init__(self, site, user=None, password=None, timeout=None,
				format=formats.JSONFormat):
		super(ShopifyConnection, self).__init__(site, user, password, timeout, format)

	def consume_token(uid, capacity, rate, min_interval=0):
	# Your rate limiting logic here
		# Get this users last UID
		last_call_time = memcache.get(uid+"_last_call_time")
		last_call_value = memcache.get(uid+"_last_call_value")
		

	def _open(self, *args, **kwargs):
		uid = self.site.split("https://")[-1].split(".myshopify.com")[0]
		self.response = None
		retries = 0
		while True:
			try:
				self.consume_token(uid, 40, 1.95, 0.05)
				self.response = super(ShopifyConnection, self)._open(*args, **kwargs)
				return self.response
			except (ConnectionError, ServerError) as err:
				retries += 1
				if retries > settings.SHOPIFY_MAX_RETRIES:
					self.response = err.response
					raise
				sleep(settings.SHOPIFY_RETRY_WAIT)


shopify.base.ShopifyConnection = ShopifyConnection