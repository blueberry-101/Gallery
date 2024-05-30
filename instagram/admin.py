from django.contrib import admin
from .models import UserInfoModel,ImageData,DummyImages, FeedbackData
# Register your models here.
@admin.register(UserInfoModel)

class useradmin(admin.ModelAdmin):
    list_display=['id','name','username','email','phone_number','password']
@admin.register(ImageData)
class imageadmin(admin.ModelAdmin):
    list_display = ['id','owner','image_name','caption','image_date_time']
@admin.register(DummyImages)
class imageadmin(admin.ModelAdmin):
    list_display = ['id','owner','image_name','caption','image_date_time']
@admin.register(FeedbackData)
class imageadmin(admin.ModelAdmin):
    list_display = ['id','game_changing_feature','contributor','like_most','flaw']