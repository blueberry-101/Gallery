from django import forms
from . import validators
from . dboperations import idinDB,usernameinDB
# create your forms here and forget about the model

class SignUpForm(forms.Form):

    # NORMAL VALIDATIONS OF FIELDS
    name = forms.CharField(
        max_length=70,
        min_length=1,
        label='',
        strip=True,
        error_messages={'required':'this field is required'},
        widget=forms.TextInput(attrs={'placeholder':'Name'}),
        required=True,

    )


    identity = forms.CharField(
        max_length=75,
        min_length=1,
        strip=True,
        label = '',
        error_messages={'required':'this field is required'},
        widget=forms.TextInput(attrs={'placeholder':'Email Address'}),
        required=True,

    )
    username = forms.CharField(
        max_length = 75,
        min_length =1,
        strip=True,
        label = '',
        widget =forms.TextInput(attrs = {'placeholder':'Username'}),
        required = True,
        )

    security = forms.CharField(
        max_length=75,
        min_length=8,
        strip=False,
        label='',
        error_messages={'required':'This field is required'},
        widget=forms.PasswordInput(attrs={'placeholder':'Password'}),
        required=True,

    )

    # CUSTOM VALIDATIONS OF SEVERAL FIELDS IN SIGNUP FORM


    def clean_identity(self):
        cleaned_identity = self.cleaned_data['identity']
        result,it_is = validators.email_or_phone(cleaned_identity)
        if not result:
            # If the it will raise error the it_is variable will be = ''
            raise forms.ValidationError(f"Invalid email or phone number details")
        if idinDB(cleaned_identity):
            raise forms.ValidationError(f'this {it_is} already exits')
        return cleaned_identity

    def clean_username(self):
        cleaned_username = self.cleaned_data['username']
        result = validators.is_valid_username(cleaned_username)
        if not result:
            raise forms.ValidationError('invalid username use numbers,alphabets and "."&"_" only')
        if usernameinDB(cleaned_username):
            raise forms.ValidationError(f'this username already exits')
        return cleaned_username
    
    def clean_security(self):
        cleaned_security = self.cleaned_data['security']
        result, missing = validators.is_valid_password(cleaned_security)
        if not result:
            raise forms.ValidationError(f"You have an error : {missing} is missing")
        return cleaned_security


class LoginForm(forms.Form):
    
    #NORMAL VALIDATORS
    identity = forms.CharField(
        max_length=70,
        min_length=1,
        label='',
        widget=forms.TextInput(attrs={'placeholder':'Username or email'}),
        error_messages={'required':'this field is required'},
        required=True,

    )
    security = forms.CharField(
        max_length=75,
        min_length=8,
        label='',
        widget=forms.PasswordInput(attrs={'placeholder':'Password'}),
        error_messages={'required':'this field is required'},
        required=True,

    )

 # THIS IS NOT ACCURATE BECAUSE IT WILL SHOW TWO FIELDS USERNOT FOUND USER THE MESSAGES FRAMEWORK TO 
 # RAISE A POP UP THAT USER NOT FOUND IF THE FORM IS INVALID WITH DISTURBING THE DATABASE hehe!

    def clean_identity(self):
        print('its working')
        cleaned_identity = self.cleaned_data['identity']
        result,it_is = validators.what_is_it(cleaned_identity)
        if not result:
            # If the it will raise error the it_is variable will be = ''
            raise forms.ValidationError("User not found")
        return cleaned_identity
    def clean_security(self):
        cleaned_security = self.cleaned_data['security']
        result, missing = validators.is_valid_password(cleaned_security)
        if not result:
            raise forms.ValidationError("User not found")
        return cleaned_security

class ConfirmPasswordForm(forms.Form):
    password1 = forms.CharField(
        max_length=75,
        min_length=8,
        label='',
        widget=forms.PasswordInput(attrs={'placeholder':'Password'}),
        error_messages={'required':'this field is required'},
        required=True,
    )
    password2 = forms.CharField(
        max_length=75,
        min_length=8,
        label='',
        widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}),
        error_messages={'required':'this field is required'},
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def clean_password1(self):
        clean_password1 = self.cleaned_data['password1']
        result, missing = validators.is_valid_password(clean_password1)
        if not result:
            raise forms.ValidationError(f"You have an error : {missing} is missing")
        return clean_password1
    
    
class ForgetPasswordForm(forms.Form):
    identity = forms.CharField(
        max_length=70,
        min_length=1,
        label='',
        widget=forms.TextInput(attrs={'placeholder':'Username or email'}),
        error_messages={'required':'this field is required'},
        required=True,
    )

    def clean_identity(self):
        print('its working')
        cleaned_identity = self.cleaned_data['identity']
        result,it_is = validators.what_is_it(cleaned_identity)
        if not result:
            # If the it will raise error the it_is variable will be = ''
            raise forms.ValidationError("User not found")
        return cleaned_identity

from django import forms

class FeedbackForm(forms.Form):
    game_changing_feature = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'game-changing-feature',
                'rows': 4,
                'required': True,
                'placeholder': '...'
            }
        ),
        label="What is one game-changing feature you want to suggest this web application?"
    )

    contributor = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'contributor',
                'placeholder': 'e.g., github/blueberry-101'
            }
        ),
        label="Do you know someone who can contribute to this web application?",
        required=False
    )

    like_most = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'like-most',
                'rows': 4,
                'required': True,
                'placeholder': '...'
            }
        ),
        label="Which feature do you like the most about this web application? & Your name!"
    )

    flaw = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'flaw',
                'rows': 4,
                'placeholder': '...'
            }
        ),
        label="Have you observed any flaws or loopholes in this web application?",
        required=False
    )

from . models import ImageData


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageData
        fields = ["image_name","caption"]
        labels = {'image_name':'Upload here '}

