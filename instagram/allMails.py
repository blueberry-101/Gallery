from django.core.mail import send_mail
from django.template.loader import render_to_string
from Finksta.settings import EMAIL_HOST
from datetime import datetime
from celery import shared_task

# working 
@shared_task
def reset_password_mail(recipient, token):
    current_year = datetime.now().year
    confirm_password_url = f'http://127.0.0.1:8000/gallery/confirmpassword/?token={token}'
    # confirm_password_url = f'https://whitegallery.up.railway.app/gallery/confirmpassword/?token={token}'
    subject = "Password Reset Link"
    html_message = render_to_string('email_templates/reset_link_mail.html', {'confirm_password_url': confirm_password_url,"year":current_year})
    plain_message = "Your internet connection is not reliable. Try again later"  # Plain text alternative

    try:
        send_mail(
            subject,
            plain_message,  # Use plain text as an alternative
            None,  # Set your sender email here if needed
            [recipient],
            html_message=html_message,
            fail_silently=True
        )
        return True
    except Exception as e:
        return e

# working    
@shared_task
def welcome_mail(recipient,name):
    current_year = datetime.now().year
    login_url = 'http://127.0.0.1:8000/'
    # login_url = 'https://whitegallery.up.railway.app/'
    subject = "Welcome To Gallery"
    html_message = render_to_string('email_templates/welcome_mail.html', {'name': name,"year":current_year,"login_url":login_url})
    plain_message = "We are so glad that you created your account here" # Plain text alternative

    try:
        send_mail(
            subject,
            plain_message,  # Use plain text as an alternative
            None,  # Set your sender email here if needed
            [recipient],
            html_message=html_message,
            fail_silently=True
        )
        return True
    except Exception as e:
        return e

# working 
@shared_task
def feedback_mail(recipient,name,post_url):
    current_year = datetime.now().year
    feedback_url = 'http://127.0.0.1:8000/gallery/feedback'
    # feedback_url = 'https://whitegallery.up.railway.app/gallery/feedback'
    subject = "We Value Your Feedback!"
    html_message = render_to_string('email_templates/feedback_mail.html', {'name': name,"year":current_year,"post_url":post_url,"feedback_url":feedback_url})
    plain_message = "Please let us know about any loopholes you have noticed, suggestions for improvements, or new features you would like to see." # Plain text alternative

    try:
        send_mail(
            subject,
            plain_message,  # Use plain text as an alternative
            None,  # Set your sender email here if needed
            [recipient],
            html_message=html_message,
            fail_silently=True
        )
        return True
    except Exception as e:
        return e

def new_user_added(recipents):
    ...

