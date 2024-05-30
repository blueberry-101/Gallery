import phonenumbers
import re
from django.core.exceptions import ValidationError
import os

def validate_image_file(image):

    # Check file extension
    valid_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif']
    ext = os.path.splitext(image.name)[1][1:].lower()  # Extract file extension and convert to lowercase
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed extensions are: {', '.join(valid_extensions)}.")
    
    # Check file size
    max_size = 5 * 1024 * 1024  # 5 MB
    if image.size > max_size:
        raise ValidationError("The image file size should not exceed 5 MB.")



def is_valid_phone_number(phonenumber):
    try:
        parsed_number = phonenumbers.parse(phonenumber,None)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False
    


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern,email):
        return True
    else:
        return False
    
def is_valid_username(username):
    pattern = r'^[a-zA-Z0-9._]{1,30}$'
    if re.match(pattern,username):
        return True
    else:
        False
        
    
def what_is_it(identity_data):
    
    if is_valid_username(identity_data):
        it_is = (True,'username')
    elif is_valid_email(identity_data):
        it_is = (True,'email')
    elif is_valid_phone_number(identity_data):
        it_is = (True,'phone_number')
    else:
        it_is = (False,'')
    return it_is

def email_or_phone(identity_data):
    
    if is_valid_phone_number(identity_data):
        it_is = (True,'phone_number')
    elif is_valid_email(identity_data):
        it_is = (True,'email')
    else:
        it_is = (False,'')
    return it_is

        
def is_valid_password(password):
    missing_criteria = []

    # Check if the password has at least one non-alphanumeric symbol
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        missing_criteria.append("non-alphanumeric symbol")

    # Check if the password has at least one numeric symbol
    if not re.search(r'\d', password):
        missing_criteria.append("numeric symbol")

    # Check if the password has at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        missing_criteria.append("uppercase letter")

    if not missing_criteria:
        return True, None
    else:
        return False, ", ".join(missing_criteria)


