from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import SignUpForm
import logging

# Setup the logger for CloudWatch
logging.basicConfig(format=
                    '%(levelname)s (%(asctime)s): file %(filename)s: line %(lineno)d: %(message)s')
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def signup_view(request):
    """sign up view to handle sign up process

    Args:
        request (request): request from urls

    Returns:
        html: render html template
    """
    LOGGER.debug("Start sign up process")
    LOGGER.debug("we get request method %s",request.method)
    # in case of post request then we need to validate the inputs
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            LOGGER.debug("sign up process are valid")
            user = form.save()
            LOGGER.debug("user saved on the db")
            # log the user in
            login(request, user)
            LOGGER.debug("user logged in")
            LOGGER.info("sign up process are valid, user logged in")
            # Now we logged in and we will redirect the user to articles list
            return redirect('articles:list')
    else:
        # we have get request and we need to show the sign up form
        LOGGER.debug("create signup form and pass it to html")
        form = SignUpForm()
    return render(request, 'users/signup.html', { 'form': form })

def login_view(request):
    """login_view to handle log in process

    Args:
        request (request): urls request

    Returns:
        html: render a template
    """
    LOGGER.debug("Start log in process")
    LOGGER.debug("we get request method %s",request.method)
    # in case of post request then we need to validate the inputs
    if request.method == 'POST':
        LOGGER.debug("start validate the auth form")
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            LOGGER.debug("valid form")
            # log the user in
            user = form.get_user()
            LOGGER.debug("get the user object")
            login(request, user)
            LOGGER.info("user logged in successfully")
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
               return redirect('articles:list')
    else:
        # we have get reqeust and we will run the log in form to the user
        LOGGER.debug("create auth form to log in throw it")
        form = AuthenticationForm()
    return render(request, 'users/login.html', { 'form': form })

def logout_view(request):
    """logout_view to handle and manage log out process

    Args:
        request (reqeust): urls request

    Returns:
        html: render tempate
    """
    LOGGER.debug("Start log out process")
    LOGGER.debug("we get request method %s",request.method)
    # Here we have only post case and when we get it we will log out the user
    if request.method == 'POST':
            logout(request)
            LOGGER.info("log out process complated successfully")
            return redirect('articles:list')
