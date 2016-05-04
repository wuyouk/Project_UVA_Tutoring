import urllib.request
import urllib.parse
import requests
from kafka import KafkaProducer
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from elasticsearch import Elasticsearch

@csrf_exempt
def search(request):
	if request.method == 'POST':
		data = request.POST
		if not data:
			return _error_response(request, "Failed.  No query received")
		query = data['query']
		es = Elasticsearch(['es'])
		result = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}})

		courses_data = result['hits']['hits']
		courses_list = []
		for c in courses_data:
			course = {}
			course['name'] = c['_source']['name']
			course['pk'] = c['_source']['pk']
			course['description'] = c['_source']['description']
			courses_list.append(course)
		#return a list dictionary (each dictionary is a course)
		return JsonResponse(courses_list, safe=False)
	else:
		es = Elasticsearch(['es'])
		result = es.search(index='listing_index', body={'query': {'query_string': {'query': 'calculus'}}, 'size': 10})
		courses_data = result['hits']['hits']
		courses_list = []
		for c in courses_data:
			course = {}
			course['name'] = c['_source']['name']
			course['pk'] = c['_source']['pk']
			course['description'] = c['_source']['description']
			courses_list.append(course)
		return JsonResponse(result, safe=False)

		return JsonResponse({'work': True, 'resp': courses_list}, safe=False)


#User: Create and return token
@csrf_exempt
def create_account(request):
	if request.method == 'POST':
		data = request.POST
		if not data:
			return _error_response(request, "Failed.  No data received")
		response = requests.post('http://models-api:8000/api/v1/user/', data = data)
		resp_data = json.loads(response.text)
		if not resp_data or not resp_data['work']:
			return _error_response(request, resp_data['msg'])
		return _success_response(request, resp_data)
	return _error_response(request, "Failed. Use post")

#User:  login user with token and return true or false
@csrf_exempt
def login(request):
	if request.method == 'POST':
		data = request.POST
		if not data:
			return JsonResponse({'fail': "no POST data received"}, safe=False)
		response = requests.post('http://models-api:8000/api/v1/authenticator/login/', data = data)
		resp_data = json.loads(response.text)
		if not resp_data or not resp_data['work']:
			# couldn't log them in, send them back to login page with error
			return _error_response(request, resp_data['msg'])
		return _success_response(request, {'authenticator': resp_data['resp']['authenticator']})
		#return JsonResponse({'login_resp': login_req}, safe=False)
	return _error_response(request, "Failed. Use post")

#User:  logout user with token and return true or false
@csrf_exempt
def logout(request):
	if request.method == 'POST':
		data = request.POST
		if not data:
			return _error_response(request, "no POST data received")
		response = requests.post('http://models-api:8000/api/v1/authenticator/logout/', data = data)
		resp_data = json.loads(response.text)
		if not resp_data or not resp_data['work']:
			return _error_response(request, resp_data['msg'])
		return _success_response(request)
	return _error_response(request, "Failed. Use post")


#User + course:  Check if user is logged in with token.  If true, post listing with token and listing text.
@csrf_exempt
def create_course(request):
	#receive authenticator
	#send authenticator
	#get user_pk or false back
	#package user_pk with course 
	#give back response I will get the UserID

	if request.method == 'POST':
		post_data = request.POST
		data = dict(post_data.dict())
		if not data:
			return _error_response("no POST data received")
		#get authenticator
		authenticator = data['authenticator']
		data_auth={'authenticator':authenticator}
		#send authenticator
		response = requests.post('http://models-api:8000/api/v1/authenticator/check/', data = data_auth)
		resp_data = json.loads(response.text)
		if not resp_data or not resp_data['work']:
			return _error_response(request, resp_data['msg'])
		#get user_pk
		tutor_pk = resp_data['resp']['tutor']
		del data['authenticator']
		data['tutor'] = tutor_pk
		data['popularity'] = 0
		course_resp = requests.post('http://models-api:8000/api/v1/course/', data = data)
		resp_data = json.loads(course_resp.text)
		if not resp_data or not resp_data['work']:
			return _error_response(request, resp_data['msg'])

		producer = KafkaProducer(bootstrap_servers='kafka:9092')
		# some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id':42}
		data['pk'] = resp_data['resp']['pk']
		producer.send('new-course-topic', json.dumps(data).encode('utf-8'))

		return _success_response(request, {'course_pk': resp_data['resp']['pk']})
	return _error_response(request, "Failed. Use post")

#Course + Tutor: get information of a list of courses
def courses(request):
	course_req = requests.get('http://models-api:8000/api/v1/course/')
	course_data = json.loads(course_req.text)
	courses_list = []
	for d in course_data:
		course = {}
		course['pk'] = d['pk']
		fields = d['fields']
		course['name'] = fields['name']
		course['description'] = fields['description']
		course['price'] = fields['price']
		tutor_pk = fields['tutor']
		user_req = requests.get('http://models-api:8000/api/v1/user/'+str(tutor_pk))
		user_data = json.loads(user_req.text)
		user = user_data['resp']
		course['tutor'] = user['name']
		course['tutor_description'] = user['description']
		courses_list.append(course)
	#return a list dictionary (each dictionary is a course)
	return JsonResponse(courses_list, safe=False)
	
#Course + Tutor: get information of a course
def course(request, course_pk = ''):
	course_req = requests.get('http://models-api:8000/api/v1/course/'+course_pk)	
	course_data = json.loads(course_req.text)
	if not course_data or not course_data['work']:
			return _error_response(request, course_data['msg'])
	course = course_data['resp']
	tutor_pk = course['tutor']
	user_req = requests.get('http://models-api:8000/api/v1/user/'+str(tutor_pk))
	user_data = json.loads(user_req.text)
	user = user_data['resp']
	data = {'course':course, 'user':user}

	# data = {'course_name':course['name'], 'course_price':course['price'], 'course_description':course['description'],'tutor_name':user['name'], 'tutor_description':user['description']}
	return _success_response(request, data)


def _error_response(request, error_msg):
	return JsonResponse({'work': False, 'msg': error_msg}, safe=False)

def _success_response(request, resp=None):
	if resp:
		return JsonResponse({'work': True, 'resp': resp}, safe=False)
	else:
		return JsonResponse({'work': True})