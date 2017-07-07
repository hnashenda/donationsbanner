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
		while True:
			try:
				#self.consume_token(uid, 40, 1.95, 0.05)
				self.consume_token(234, 40, 1.95, 0.05)
				self.response = super(ShopifyConnection, self)._open(*args, **kwargs)
				return self.response
			except (ConnectionError, ServerError) as err:
				retries += 1
				if retries > settings.SHOPIFY_MAX_RETRIES:
					self.response = err.response
					raise
				sleep(settings.SHOPIFY_RETRY_WAIT)


shopify.base.ShopifyConnection = ShopifyConnection