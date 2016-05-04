def login(request):
    if request.method == 'GET':
      next = request.GET.get('next') or reverse('home')
      return render('login.html', ...)
    f = login_form(request.POST)
    if not f.is_valid():
      # bogus form post, send them back to login page and show them an error
      return render('login.html', ...)
    username = f.cleaned_data['username']
    password = f.clearned_data['password']
    next = f.cleaned_data.get('next') or reverse('home')
    resp = login_exp_api (username, password)
    if not resp or not resp['ok']:
      # couldn't log them in, send them back to login page with error
      return render('login.html', ...)
    # logged them in. set their login cookie and redirect to back to wherever they came from
    authenticator = resp['resp']['authenticator']
    response = HttpResponseRedirect(next)
    response.set_cookie("auth", authenticator)
    return response

def create_listing(request):
    auth = request.COOKIES.get('auth')
    if not auth:
      # handle user not logged in while trying to create a listing
      return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing")
    if request.method == 'GET':
      return render("create_listing.html", ...)
    f = create_listing_form(request.POST)
    ...
    resp = create_listing_exp_api(auth, ...)
    if resp and not resp['ok']:
        if resp['error'] == exp_srvc_errors.E_UNKNOWN_AUTH:
            # exp service reports invalid authenticator -- treat like user not logged in
            return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing")
     ...
     return render("create_listing_success.html", ...)