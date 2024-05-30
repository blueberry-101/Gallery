from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpRequest
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .forms import SignUpForm, LoginForm, ConfirmPasswordForm, ForgetPasswordForm, FeedbackForm  # Importing forms
from .models import UserInfoModel, FeedbackData  # Importing models
from .validators import what_is_it  # Importing validators
from .dboperations import idinDB, foundinDB, saveinDB, changePassword, findEmailinDB, add_dummy_images, checkfirstpost  # Importing database operations
from .middlewares import is_user_middleware  # Importing middleware
from .restrictions import restrict_ten_image,image_restrict_forever  # Importing Restrictions
from .allMails import reset_password_mail, welcome_mail, feedback_mail
from .important import mask_email
from .jwt_configs import jwt_is_expired

from jwt import encode, decode  # Importing JWT functions
from datetime import datetime,timezone,timedelta
###################### VIEWS ##########################

from Finksta.settings import SECRET_KEY

# SECERT = "secret"
SECERT = SECRET_KEY

# SIGNUP VIEWS

class SignUpClass(View):

    # Handling GET request for signup
    def get(self, request:HttpRequest):
        try:
            token = request.COOKIES.get('uid')
            decoded_token = decode(token, SECERT, algorithms=['HS256'], verify=True)
            print("token verified in login")
            username = decoded_token.get("username")
            response = HttpResponseRedirect(reverse('feedpage', kwargs={'username': username}))
            return response
        except:
            print('token not verified in signup view')
            signupfm = SignUpForm()
            context =  {'signupfm': signupfm}
            return render(request, 'signup.html',context)

    # Handling POST request for signup
    def post(self, request:HttpRequest):
        signupfm = SignUpForm(request.POST)
        if signupfm.is_valid():
            nm = signupfm.cleaned_data['name']
            usernm = signupfm.cleaned_data['username']
            pswd = signupfm.cleaned_data['security']
            id = signupfm.cleaned_data['identity']
            if idinDB(id):
                ErrorExistence = f'{what_is_it(id)[1]} already exits, try to login'
                signupfm = SignUpForm()
                context = {'signupfm': signupfm, "Errors": ErrorExistence}
                return render(request, 'signup.html', context)
            else:
                saveinDB(nm, usernm, id, pswd)
                # add dummy images to this account.
                usermodel_instance = UserInfoModel.objects.get(username=usernm)
                add_dummy_images(usermodel_instance)
                welcome_mail.delay(usermodel_instance.email,usermodel_instance.name)
                return redirect('loginpage')
        else:
            return render(request, 'signup.html', {'signupfm': signupfm})

# LOGIN VIEW

class LoginClass(View):

    # Handling GET request for login
    def get(self, request:HttpRequest):
        try:
            print("request.content_params",request.content_params)
            token = request.COOKIES.get('uid')
            decoded_token = decode(token, SECERT, algorithms=['HS256'], verify=True)
            print("token verified in login")
            username = decoded_token.get("username")
            response = HttpResponseRedirect(reverse('feedpage', kwargs={'username': username}))
            return response
        except:
            print('token not verified in login view')
            loginfm = LoginForm()
            context = {'loginfm': loginfm}
            return render(request, 'index.html', context)

    # Handling POST request for login
    def post(self, request):
        loginfm = LoginForm(request.POST)
        if loginfm.is_valid():
            id = loginfm.cleaned_data['identity']
            pswd = loginfm.cleaned_data['security']
            # Verifying credentials in the database
            result, it_is = foundinDB(id, pswd)
            if not result:
                notfound = f'{it_is} & password not found'
                loginfm = LoginForm()
                context = {'loginfm': loginfm, 'notfounderror': notfound}
                return render(request, 'index.html', context)
            else:
                lookup_username_field = {it_is: id}
                userobject = UserInfoModel.objects.get(**lookup_username_field)
                username = UserInfoModel.objects.get(**lookup_username_field).username
                identity_dict = request.POST
                identity = identity_dict.get("identity")
                encoded_jwt = encode({"uid": identity, "username": username}, SECERT, algorithm="HS256")
                response = HttpResponseRedirect(reverse('feedpage', kwargs={'username': username}))
                response.set_cookie("uid", encoded_jwt, httponly=True)
                # send welcome mail
                
                # feedback_mail.delay(userobject.email,userobject.name)
                return response
        else:
            return render(request, 'index.html', {'loginfm': loginfm})

# LOGOUT

def logout_view(request:HttpRequest):
    response = redirect("loginpage")
    response.delete_cookie('uid')
    print('logout occurred')
    return response

# FEED
from .forms import ImageForm
from .models import ImageData
from .models import DummyImages

@is_user_middleware
def showfeed(request:HttpRequest, username):
    print(request.user)
    print("request.content_params",request.GET)
    userobject = UserInfoModel.objects.get(username=username)
    page_number = request.GET.get("page","1")

    if request.method == "POST":
        # total 50 posts allowed
        restriction1 = image_restrict_forever(request=request,username=username)
        if restriction1:
            return redirect(reverse('feedpage', kwargs={'username': username}) + f'?page={request.GET.get("page","1")}')
        else:
            ...

        # image post restriction : One week 10 images allowed
        restriction2 = restrict_ten_image(request=request,username=username)  
        if restriction2 is not None:
            return redirect(reverse('feedpage', kwargs={'username': username}) + f'?page={request.GET.get("page","1")}')
        
        # Passed every restrictions
        else:
            filled_image_form = ImageForm(request.POST, request.FILES)
            if filled_image_form.is_valid():
                this_image_data = filled_image_form.save(commit=False)
                this_image_data.owner = userobject    # what is this doing here? telling which user to choose
                try:
                    this_image_data.save()
                    try:
                        if checkfirstpost(username):
                            feedback_mail.delay(userobject.email,userobject.name,this_image_data.image_name.url)
                    except Exception as e:
                        print("exception in the first image post",e)
                    messages.success(request,"Your Image Posted Successfully")
                except Exception as e:
                    print(e)
                response = redirect(reverse('feedpage', kwargs={'username': username}) + f'?page={request.GET.get("page","1")}')
                return response
            else: # Invalid Form handling
                # Handled Max File size error
                error = filled_image_form.errors
                print("error",error)
                for e in error.values():
                    messages.error(request,e)
                response = redirect(reverse('feedpage', kwargs={'username': username}) + f'?page={request.GET.get("page","1")}')
                return response
                
    if request.method == "GET":
        name = userobject.name
        image_objects = userobject.user_images.all().order_by('image_date_time')
        dummy_objects = userobject.user_dummy_images.all().order_by('image_date_time')

        dummy_paginator = Paginator(dummy_objects,20)
        try:
            dummy_page = dummy_paginator.get_page(1)
        except Exception as e:
            print("Something went wrong in dummy pagination:", e)

        # Paginate image_objects
        image_paginator = Paginator(image_objects,8)
        try:
            image_page = image_paginator.get_page(1)
        except Exception as e:
            print("Something went wrong in image pagination:", e)

            # Merge paginated results
        try:
            combined_objects =  list(dummy_page.object_list) + list(image_page.object_list)
        except Exception as e:
            print("Error combining paginated results:", e)

        # Combine paginated results
        combined_paginator = Paginator(combined_objects, 8)
        try:
            combined_page = combined_paginator.get_page(page_number)
        except Exception as e:
            print("Something went wrong in combined pagination:", e)
        # for image in combined_page:
            # print("adaadad",image.__str__())
        # Image Post Form
        print("feedfeed")
        empty_image_form = ImageForm()
        return render(request, template_name='feed.html', context={"form": empty_image_form, "images": combined_page,"nameofuser": name,"username":username})

@is_user_middleware   
def image_detail(request:HttpRequest, username,imagetype,image_id,page_number):

    print("image_type",imagetype)
    try:
        print("username of context",username)
        print("dpaegnumber",page_number)
        if imagetype == "dimage":
            image = DummyImages.objects.get(id=image_id)
        else:
            image = ImageData.objects.get(id=image_id)
        return render(request, 'imagecard.html', {'image': image,'page_number':page_number,"username":username})
    except Exception as e:
        path = request.path
        print("error in dimage",e)
        return redirect("pagenotfound",path=f"{path}")


def delete_image(request:HttpRequest,imagetype,image_id,page_number):
    # print("image type",imagetype)
    if imagetype == "dimage":
        image_obj = DummyImages.objects.get(id=image_id)
    else:
        image_obj = ImageData.objects.get(id=image_id)
    try:
        image_obj.delete()  # code to delete image instance from DB along with file
        print(request.user)
        messages.success(request,"Image Deleted Sucessfully")
    except Exception as e:
        print("HANDLE IT : image didn't deleted",e)
    finally:
        username = image_obj.owner                  
        return redirect(reverse('feedpage', kwargs={'username': username}) + f'?page={page_number}')
    

# 404 Error Page
def page_not_found(request:HttpRequest, path=None):
    return render(request, template_name="page-unavailable.html")


# Policies Page
def policies(request:HttpRequest):
    from .important import build_absolute_uri
    login_url = build_absolute_uri('feedback',)
    print(login_url)

    return render(request, template_name="privacy&policy.html")

@method_decorator(csrf_exempt, name='dispatch')
class ConfirmPassword(View):
    def get(self,request:HttpRequest, *args, **kwargs):
        try:
            token = request.GET.get("token")
            payload = decode(token,SECERT,algorithms="HS256",options={"verify_signature": False})
            if jwt_is_expired(payload):
                path = request.path
                return redirect("pagenotfound",path=path)
        except Exception as e:
            print(e)
            path = request.path
            return redirect("pagenotfound",path=path)
        else:
            confirm_pass_form = ConfirmPasswordForm()
            context = {"form":confirm_pass_form}
            return render(request,template_name="confirmpassform.html",context=context)
    
    # @method_decorator(csrf_exempt)
    def post(self,request:HttpRequest, *args, **kwargs):
        filled_form = ConfirmPasswordForm(request.POST)
        if filled_form.is_valid():
            token = request.GET.get("token")
            try:
                payload = decode(token,SECERT,algorithms="HS256",options={"verify_signature": False})              
                if jwt_is_expired(payload):
                    path=request.path
                    return redirect("pagenotfound",path)
                else:
                    ...
                
                email = payload.get("email")
                e = changePassword(email,filled_form.cleaned_data.get("password1"))
                print(e)
                return redirect("loginpage")
            except Exception as e:
                print("while posting form",e)
                context = {"errors":e,"form":filled_form}
                return render(request,template_name="confirmpassform.html",context=context)

        else:
            context = {"form":filled_form}
            return render(request,template_name="confirmpassform.html",context=context)

def generateToken(email:str,secret:str,expiration_minutes:int)->str:
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    payload = {"email":email,'exp': expiration_time}
    token = encode(payload,secret,algorithm="HS256")
    reset_link = token
    return reset_link

def forget_password(request:HttpRequest):
    
    if request.method == "GET":
        identity_form = ForgetPasswordForm()
        context = {"form":identity_form}
        return render(request,template_name="resetpassform.html",context=context)

    if request.method == "POST":
        filled_identity_form = ForgetPasswordForm(request.POST)
        if filled_identity_form.is_valid():
            identity = filled_identity_form.clean_identity()
            result,email=findEmailinDB(identity)
            print("result,email",result,email)
            if result:
                print(email)
                token = generateToken(email,SECERT,60)
                reset_password_mail.delay(email,token)
                context = {"mask_email":mask_email(email)}
                return render(request,template_name="emailsentpage.html",context=context)
            else:
                messages.error(request,"User not having email")
                return redirect("resetpassword")

        else:
            errorss = filled_identity_form.errors
            messages.error(request,errorss)
        return render(request,template_name="resetpassform.html",context={"form":filled_identity_form})

def feedback_view(request:HttpRequest):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            game_changing_feature = form.cleaned_data['game_changing_feature']
            contributor = form.cleaned_data['contributor']
            like_most = form.cleaned_data['like_most']
            flaw = form.cleaned_data['flaw']
            feedback_data = FeedbackData(
                game_changing_feature=game_changing_feature,
                contributor=contributor,
                like_most=like_most,
                flaw=flaw
            )
            feedback_data.save()
            return render(request, "feedbacksubmitted.html")  # Redirect to a thank you page or elsewhere
        else:
            return render(request, 'feedbackpage.html', {'form': form})
    else:
        form = FeedbackForm()
    return render(request, 'feedbackpage.html', {'form': form})

