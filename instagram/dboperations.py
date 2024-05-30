from .validators import what_is_it
from . models import UserInfoModel, DummyImages, ImageData
from django.db.models import Q
def usernameinDB(usernm):
    username_exits = UserInfoModel.objects.filter(username=usernm).exists()
    if username_exits:
        return True
    else:
        return False



def idinDB(identity):
    result,it_is = what_is_it(identity)
    if it_is=='username':
        id_in_database = UserInfoModel.objects.filter(username=identity).exists()
    elif it_is== 'email':
        id_in_database = UserInfoModel.objects.filter(email=identity).exists()
    elif it_is == 'phone_number':
        id_in_database = UserInfoModel.objects.filter(phone_number=identity).exists()
    else:
         id_in_database = result
    return id_in_database

# LOOP HOLE 1 : THIS WILL NOT CHECK WHETHER THE 'PASSWORD' IS OF 'ID' OR NOT {SORTED OUT}

def foundinDB(id,pswd):
    result,it_is = what_is_it(id)
    if it_is=='username':
        user_in_database = UserInfoModel.objects.filter(username=id,password=pswd).exists()
    elif it_is== 'email':
        user_in_database = UserInfoModel.objects.filter(email=id,password=pswd).exists()
    elif it_is == 'phone_number':
        user_in_database = UserInfoModel.objects.filter(phone_number=id,password=pswd).exists()
    else:
         user_in_database = result
    return user_in_database,it_is


def saveinDB(nm,usernm,id,pswd):
            result,it_is = what_is_it(id)
            if it_is== 'email':
                database = UserInfoModel(name = nm,username=usernm,password = pswd,email = id)
            elif it_is == 'phone_number':
                database = UserInfoModel(name = nm,username=usernm,password = pswd,phone_number = id)             
            
            database.save()
            return result

def changePassword(given_email,newpassword:str)->str:
    try:
        user_obj = UserInfoModel.objects.get(email=given_email)
        user_obj.password = newpassword
        user_obj.save()
        return "Successfully Changed Password"
    except Exception as e:
         return f"{e}" 

def findEmailinDB(identity):
    result, it_is = what_is_it(identity)
    if it_is == "username":
        try:
            email = UserInfoModel.objects.get(username=identity).email
            return result,email
        except Exception as e:
             print("ehre")
             return False,e
    elif it_is == "email":
        try :
            result = UserInfoModel.objects.filter(email=identity).exists()
            return result,identity
        except Exception as e:
            return False,e
    else:
        return result,identity


def add_dummy_images(usermodel):
    try:
        # Check if there are any dummy images to copy
        all_dummy_images = DummyImages.objects.filter(owner__isnull=True)

        if all_dummy_images.exists():
            for image_instance in all_dummy_images:
                # Create a new instance of DummyImages
                new_image_instance = DummyImages(
                    # Copy fields from the existing image_instance
                    image_name=image_instance.image_name,
                    caption=image_instance.caption,
                    image_date_time = image_instance.image_date_time,
                    # Set the owner to the provided usermodel
                    owner=usermodel
                )
                # Save the new instance to the database
                new_image_instance.save()
    except Exception as e:
        print("Exception in DB OPERATIONS add_dummy_images:", e)

def checkfirstpost(username):
    total_posted_images = ImageData.objects.filter(owner__username=username).count()
    if total_posted_images <= 1:
        return True
    else:
        return False