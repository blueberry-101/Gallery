from django.db import models
from .validators import validate_image_file
from django.core.validators import FileExtensionValidator
from cloudinary.models import CloudinaryField
from cloudinary import api

# Create your models here.
class UserInfoModel(models.Model):
    name = models.CharField(max_length=75,)
    username = models.CharField(max_length=75,unique=True,null=True)
    phone_number = models.CharField(max_length=75,unique=True,null=True)
    email = models.EmailField(unique=True,null=True)
    password = models.CharField(max_length=75)
    def __str__(self):
        return self.username

class ImageData(models.Model):
    owner = models.ForeignKey(UserInfoModel,on_delete = models.CASCADE,related_name = "user_images")
    # image_name = models.ImageField(upload_to="images",validators = [FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    image_name = CloudinaryField(
        "images",
        folder=f"gallery",
        validators=[
            validate_image_file,
        ],
    )
    caption = models.CharField(max_length=40)
    image_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "image"
    

    
    """    def delete(self, *args, **kwargs):
        # Delete the image file from storage
        if self.image_name:
            if path.isfile(self.image_name.path):
                remove(self.image_name.path)
        # Call the parent class' delete method
        super().delete(*args, **kwargs)
        
    """
    def delete(self, *args, **kwargs):
        # Delete the image from Cloudinary when the instance is deleted
        api.delete_resources([self.image_name.public_id])
        super().delete(*args, **kwargs)

 
class DummyImages(models.Model):
    owner = models.ForeignKey(UserInfoModel,on_delete = models.CASCADE,related_name = "user_dummy_images",null=True, blank=True)
    image_name = CloudinaryField(
        "dimage",
        folder="dummyimages",
    )
    caption = models.CharField(max_length=40)
    image_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "dimage"
    
class FeedbackData(models.Model):
    game_changing_feature = models.TextField(verbose_name="Game-changing Feature")
    contributor = models.CharField(max_length=255, blank=True, verbose_name="Contributor")
    like_most = models.TextField(verbose_name="Like Most")
    flaw = models.TextField(blank=True, verbose_name="Flaw")

    def __str__(self):
        return f"Feedback {self.like_most}"
