from django.shortcuts import render
from shopify_auth.decorators import login_required
from django.http import HttpResponse
import shopify
import json
#from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
@xframe_options_exempt
@login_required
def home(request, *args, **kwargs):
	orders=[]
	#with request.user.session:
		#products = shopify.Product.find()
	#	orders = shopify.Order.find()	
	return render(request, "my_app/home.html", {
		'orders': orders,
	})

	
#@json_response
@xframe_options_exempt
#@login_required
def featured(request, *args, **kwargs):
	#auth_login(request, user)
	#data = {'foo': 'bar', 'hello': 'world'}
	orders=[]
	num = 204
	
	
	
	#request = requests.Session(auth=(settings.SHOPIFY_API_KEY, settings.SHOPIFY_API_PASSWORD))
	#print request
	#print json.loads(request.get('http://myshop.myshopify.com/admin/assets.json').content)
	#response = HttpResponse(json.dumps({"key": "value", "key2": "value"}))
	#response["Access-Control-Allow-Origin"] = "http://jsfiddle.net/yvzSL/"
	#response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	#response["Access-Control-Max-Age"] = "1000"
	#response["Access-Control-Allow-Headers"] = "*"
	#for item in seq:
	#	num+=len(item.line_items)
	#return num
	#if !request.user.is_authenticated:
	#	return render(request, "my_app/home.html")
	

	
	with request.user.session:
		#products = shopify.Product.find()
		orders = shopify.Order.find()
	for item in orders:
		num+=len(item.line_items)
	data = {'count':num}
	
	#return response
	if 'callback' in request.REQUEST:
		data = '%s(%s);' % (request.REQUEST['callback'], data)
		return HttpResponse(data, content_type="application/json")
	return HttpResponse(json.dumps(data), content_type='application/json')
	#response = request.post('http://testhuber.myshopify.com/admin/products', data=payload,	headers={'
	#	'Content-Type': 'application/json', # this is the important part.
	#'},)
	#print response.status_code, response.content
#SHOPIFY_APP_API_KEY = '0ce24ad619b8c127fa0bf56846165c2c'
#SHOPIFY_APP_API_SECRET = os.environ.get('8bacf8d2664ce3311e6c96dffe992ed6')
#SHOPIFY_APP_API_SECRET = '436a28e2adaaf666f6eb50b4f08c2784'	
def donations(request, *args, **kwargs):
	#api_key = '0ce24ad619b8c127fa0bf56846165c2c'
	#api_secret = '55fe4a50f4ace3569ed530c9f8986c27' 
	#reqParams = request.GET.copy()
	#if not proxy_signature_is_valid(request, api_secret):
	#	raise Exception('Invalid signature.')	
	#signature = reqParams.get('signature', '') 
	#del reqParams['signature'] 
	#sorted_params = ''.join(sorted(["%s=%s" % (key, ','.join(val)) 
#for key, val in reqParams.iterlists()]))
	#checkSig = hmac.new(api_secret, sorted_params, hashlib.sha256) 
	#err = (checkSig.hexdigest() != signature) 
	#if err: 
	#	raise Exception("Shopify Proxy request is not authentic. Signature mismatch.")
	#if not proxy_signature_is_valid(request, '436a28e2adaaf666f6eb50b4f08c2784'):
	#	raise Exception(request)
		#return HttpResponse("error on page")
		#pdb.set_trace()
	orders=[]
	#context = get_context_data()       
	#import shopify
	#shop = shopify.Shop.current()
	# Get a list of the user's products.
	#self.render_to_response(context, content_type="text/xml; charset=utf-8")
	with request.user.session:
		#products = shopify.Product.find()
		orders = shopify.Order.find()
	return render(request, "my_app/donations.html", {
		'orders': orders,
	})

