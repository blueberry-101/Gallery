#To activated the middleware add middleware into settings.py
# INITIALIZATION HAPPENS IN EVERY MIDDLE WARE FROM DOWN TO UP AS THEY ARE WRITTEN IN SETTINGS.PY
#THEN: in every middle ware they execute the code before view
# like- brother,father ,mother after view as in settings.py
#THEN: in every middle ware they excute the code  after view from last
# like- mother, father ,brother after view as in settings.py
# Learn like - neeche upar neeche in settings.py
from django.shortcuts import redirect
from functools import wraps
from jwt import decode
from django.urls import reverse
from django.http import HttpRequest
from Finksta.settings import SECRET_KEY
# SECERT = "secret"
SECERT = SECRET_KEY

def is_user_middleware(get_response):
    print("This is initialization")

    @wraps(get_response)
    def middleware(request:HttpRequest, *args, **kwargs):
        print("This before view")
        
        # Check if the request is for the login page
        if request.path == reverse("loginpage"):
            return get_response(request, *args, **kwargs)
        
        try:
            # checking presence of valid token
            print("checking token")
            token = request.COOKIES.get('uid')
            print("token found")
            decoded_token = decode(token, SECERT, algorithms=['HS256'], verify=True)
            print("token verified in middleware", decoded_token)
            print("jhjh",kwargs.get("username"))
            # checking presence 
            payload = decoded_token.get("username")
            if payload == kwargs.get("username"):
                # if payload == request.path_info
                print("token verified in middleware", decoded_token)
                response = get_response(request, *args, **kwargs)
                print("This is after view")
                return response
            else:
                return redirect('pagenotfound',request.path)
        except Exception as e:
            print("exception occurred in middleware:",e)
            return redirect('loginpage')

    return middleware

               
    return middleware
# MIDDLE WARE HOOKES
    
#middlewares are those logics requests and responses globally before they reach 
#the view or after the view has processed the request. 
    