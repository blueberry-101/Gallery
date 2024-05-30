from django.urls import path
from .views import LoginClass,SignUpClass,ConfirmPassword,showfeed,logout_view,page_not_found,policies,image_detail,delete_image,forget_password, feedback_view
from . import views
# added after image feature
from django.conf.urls.static import static
from django.conf import settings

from django.conf.urls import handler404
handler404 = page_not_found
nonStaticURL = [    
    path('', LoginClass.as_view() , name="loginhomepage"),
    path('gallery/login' , LoginClass.as_view() , name="loginpage"),
    path('gallery/signup',SignUpClass.as_view(),name='signuppage'),
    path('gallery/<str:username>/feed',showfeed,name='feedpage'),
    path('gallery/logout',logout_view,name='logout'), 
    path("gallery/policies",policies,name="policiespage"),
    path("gallery/<str:username>/<str:imagetype>/view/<int:image_id>/<str:page_number>",image_detail,name="dimagepage"),
    path("gallery/image/<str:imagetype>/delete/<int:image_id>/<str:page_number>",delete_image,name="deleteimage"),
    path("gallery/resetpassword",forget_password,name="resetpassword"),
    path("gallery/confirmpassword/",ConfirmPassword.as_view(),name="confirmpassword"),
    path('gallery/feedback', feedback_view, name='feedback'),
]

#added after image feature
StaticURL = static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns = nonStaticURL + StaticURL +[path("<path:path>",page_not_found,name="pagenotfound")]


