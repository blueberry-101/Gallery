from django.contrib import messages
from .models import ImageData
from datetime import datetime,timedelta
from typing import Optional 
# You cannot post more than 50 images.
def image_restrict_forever(request,username:str)->bool:
    try:
        total_images = ImageData.objects.filter(owner__username=username).count()

    except Exception as e:
        print("exception occured in restiction 1",e)
    else:
        print("total_images in the gallery in restrictin 1",total_images)
        if total_images > 50:
            messages.info(request,"You have Maximum images in your gallery Bro! ")
            return True
        else:
            return False


# Find the date of last 10th photo and return (datetime+7).day or None

def restrict_ten_image(username:str,request)->Optional[bool]:
    try:
        image = ImageData.objects.filter(owner__username = username).order_by("id")[20]
        datetime_10th_image = image.image_date_time.date()
        today_datetime = datetime.today().date()
        difference = (today_datetime-datetime_10th_image).days

    except Exception as e:
        print("exception occured in restriction 2",e)
        return None
    
    else:

        # logic
        if difference<7:
            eligible_date = datetime_10th_image + timedelta(days=7)
            day = eligible_date.strftime("%A")
            messages.info(request,f"You can Post other images next week on {day}")
            print("You can upload after 7 days only",day)
            return True
        else:
            return None

