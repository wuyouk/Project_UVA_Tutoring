from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import urllib.request
import urllib.parse
import json
import requests
import socket
from django.core.urlresolvers import reverse
from .forms import SignupForm, LoginForm, ListingForm, SearchForm
from django.http import HttpResponseRedirect                                                                                                                                                        # note, no timeouts, error handling or all the other things needed to do this for real                                                                                                                      


#Notes: currently no timeouts, error handling or all the other things needed to do this for real                                                                                                                      

#Home: currently no service-oriented home page 
def home(request):
    try:
        hostname = socket.gethostname()
    except:
        hostname = 'localhost'
    testing = {"hostname":hostname}
    return render(request, 'home.html', testing)

#Course-GET: Use course service to get information of a course
def course_info(request, pk = ''):
    #Method1 with requests:
    course_req = requests.get('http://exp-api:8000/v1/course/'+pk)
    course_data = json.loads(course_req.text)
    # course = course_data['resp']
    return render(request, 'course_info.html', course_data['resp'])
    #Method2 with urllib:
    # req = urllib.request.Request('http://exp-api:8000/course/'+pk)
    # resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    # resp = json.loads(resp_json)
    # context_dict = resp
    # return render(request, 'course_info.html', context_dict)

#Courses-GET: Use courses service to get information of all courses
#Notes: may need to change to base on search options
def courses_info(request):
    courses_req = requests.get('http://exp-api:8000/v1/courses/')
    courses = json.loads(courses_req.text)
    return render(request, 'courses_info.html', {'courses': courses})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup.html', {'form':form, 'error':'Please complete the form correctly'})
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            description = form.cleaned_data['description']
            data = {'grade': 0,'name': name, 'password':password, 'email':email, 'phone':phone, 'description':description}
            response = requests.post('http://exp-api:8000/v1/account/create/', data = data)
            resp_data = json.loads(response.text)
            if not resp_data or not resp_data['work']:
                return render(request, 'signup.html', {'form':form, 'error':resp_data['msg']})
                return JsonResponse(request, resp_data['msg'])
            auth = request.COOKIES.get('auth')
            if auth:
                return HttpResponseRedirect(reverse("home"))
            return HttpResponseRedirect(reverse("login"))
    #urllib.request.Request('http://exp-api:8000/product'+info)
    else: 
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'GET':
        # if a user is already login, log the user out first
        auth = request.COOKIES.get('auth')
        if auth:
            return HttpResponseRedirect(reverse("logout"))
        form = LoginForm()
        next = request.GET.get('next') or reverse('home')
        return render(request,'login.html', {'form':form})
    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, 'login.html', {'form':form, 'error':'The username and password you entered did not match our records. Please double-check and try again.'})
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    next = form.cleaned_data.get('next') or reverse('home')
    data = {'email':email, 'password':password}
    resp = requests.post('http://exp-api:8000/v1/login/', data = data)
    resp_data = json.loads(resp.text)
    if not resp_data or not resp_data['work']:
      # couldn't log them in, send them back to login page with error
        return render(request, 'login.html', {'form':form, 'error':resp_data['msg']})
    authenticator = resp_data['resp']['authenticator']
    response = HttpResponseRedirect(next)
    response.set_cookie("auth", authenticator)
    return response

def user_logout(request):
    # delete cookie and authenticator
    auth = request.COOKIES.get('auth')
    if not auth:
        # handle user not logged in while trying to logout
        return HttpResponseRedirect(reverse("login"))
    data = {'authenticator': auth}
    resp = requests.post('http://exp-api:8000/v1/logout/', data = data)
    resp_data = json.loads(resp.text)
    if resp_data['work']:
        response = HttpResponseRedirect(reverse("home"))
        response.delete_cookie('auth')
        response.delete_cookie('csrftoken')
        return response 
        # return render(request, 'home.html', {'success': 'You have been logged out.'})
    response = HttpResponseRedirect(reverse("home"))
    response.delete_cookie('auth')
    response.delete_cookie('csrftoken')
    return response
    # return JsonResponse({'result': resp_data}, safe=False)

def listing(request):
    auth = request.COOKIES.get('auth')
    if not auth:
        # handle user not logged in while trying to create a listing
        return HttpResponseRedirect(reverse("login") + "?next=" + reverse("listing"))
    if request.method == 'GET':
        form = ListingForm()
        return render(request, "listing.html", {'form':form})
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if not form.is_valid():
            # form = ListingForm()
            return render(request, "listing.html", {'form':form, 'error':'Please complete the form correctly'})
        name = form.cleaned_data['course_name']
        tag = form.cleaned_data['tag']
        description = form.cleaned_data['description']
        qualification = form.cleaned_data['qualification']
        time = form.cleaned_data['times']
        price = form.cleaned_data['price']
        data = {'authenticator':auth, 'name':name, 'tag':tag, 'description':description, 'qualification':qualification, 'time':time, 'price':price}
        resp = requests.post('http://exp-api:8000/v1/course/create/', data = data)
        resp_data = json.loads(resp.text)
        if not resp_data or not resp_data['work']:
                # exp service reports invalid authenticator -- treat like user not logged in
                return HttpResponseRedirect(reverse("login") + "?next=" + reverse("listing"))
        return HttpResponseRedirect(reverse("course_info")+str(resp_data['resp']['course_pk']))
        return render(request, "listing.html", {'form':form, 'success': 'Your course has been created.'})

def search(request):
    courses_req = requests.get('http://exp-api:8000/v1/courses/')
    courses = json.loads(courses_req.text)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if not form.is_valid():
            return render(request, "search.html", {'error':'Please enter a search query'})
        query = form.cleaned_data['query']
        data = {'query':query}
        resp = requests.post('http://exp-api:8000/v1/search/', data = data)
        resp_data = json.loads(resp.text)
        #if not resp_data or not resp_data['work']:
        #    return render(request, 'search.html', {'form':form, 'error':resp_data['msg']})
        return render(request, 'search.html', {'courses': resp_data})
    else: 
        return render(request, 'search.html')