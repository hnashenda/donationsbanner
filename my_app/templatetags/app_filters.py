from django import template
from datetime import date, timedelta
import hashlib, base64, hmac

register = template.Library()

 #for item in seq:
     #   if not item:
      #      continue
       # num += 1
        #yield num, item

@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value+arg

@register.filter(name='filteriternum')	
def filteriternum(seq):
	num = 204
	for item in seq:
		num+=len(item.line_items)
	return num

#@register.filter(name='featured')		
#def featured(request):
#	response = HttpResponse("", content_type="application/liquid; charset=utf-8")
#	response['Content-Length'] = len(content)
#	response.write('<html>test123</html>')
#	return response
@register.filter(name='get_proxy_signature')
def get_proxy_signature(query_dict, secret):
    """
    Calculate the signature of the given query dict as per Shopify's documentation for proxy requests.
    See: http://docs.shopify.com/api/tutorials/application-proxies#security
    """

    # Sort and combine query parameters into a single string.
    sorted_params = ''
    for key in sorted(query_dict.keys()):
        sorted_params += "{0}={1}".format(key, ",".join(query_dict.getlist(key)))

    signature = hmac.new(secret, sorted_params, hashlib.sha256)
    return signature.hexdigest()

@register.filter(name='proxy_signature_is_valid')
def proxy_signature_is_valid(request, secret):
    """
    Return true if the calculated signature matches that present in the query string of the given request.
    """

    # Create a mutable version of the GET parameters.
    query_dict = request.GET.copy()

    # Extract the signature we're going to verify. If no signature's present, the request is invalid.
    try:
        signature_to_verify = query_dict.pop('signature')[0]
    except KeyError:
        return False

    calculated_signature = get_proxy_signature(query_dict, secret)

    # Try to use compare_digest() to reduce vulnerability to timing attacks.
    # If it's not available, just fall back to regular string comparison.
    try:
        return hmac.compare_digest(calculated_signature, signature_to_verify)
    except AttributeError:
        return calculated_signature == signature_to_verify