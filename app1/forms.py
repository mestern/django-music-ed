# imports forms to make my forms
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

# import my models from models.py
from .models import *

# give me accesses to users data in database
from django.contrib.auth.models import User


class TicketForm(forms.Form):
    SUBJECT_CHOICES = [
        ('SUG', 'suggestions'),
        ('CRT', 'criticism'),
        ('REP', 'report')
    ]
    name = forms.CharField(max_length=50, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True)
    phone = forms.CharField(max_length=11, required=True)
    email = forms.EmailField(max_length=250, required=False)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('Enter a Valid Phone Number')

        return phone


# make a form using froms.Form
class PostCreateForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model=Post
        fields = ['title', 'description', 'file']

    # I need to define each field
    # title = forms.CharField(max_length=30, required=True)
    #
    # description = forms.CharField(widget=forms.Textarea, required=True)
    # file = forms.FileField(required=False)
    #

    # a custom validation :
    # def clean_auth(self):
    #     auth = self.cleaned_data['auth']
    #     if auth:
    #         try:
    #             User.objects.get(username=auth)
    #             return auth
    #
    #         except:
    #             raise forms.ValidationError('Enter a Valid username')


# make a form using forms.ModelForm
class CommentFrom(forms.ModelForm):
    # custom validation :
    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if name:
    #         if len(name) >= 30:
    #             raise forms.ValidationError(', (Name Had To Between 0 and 30 Character)')
    #
    #     return name

    class Meta:
        model = Comment
        fields = ['name', 'message']

        # using widgets to make some edit on forms
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'name'
                # i can to give class or placeholder or anything else...
            }
            )
        }

class SearchForm(forms.Form):
    query = forms.CharField()


# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ['image', ]

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "usrname or password is incorrect",
        "inactive": "This account is inactive. Please contact support.",
    }


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)
    class Meta:
        model = User
        fields = ['username', 'email',]

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", self.error_messages["password_mismatch"])
        else:
            # Run Django's password validators on password1
            try:
                validate_password(password1, self.instance)
            except forms.ValidationError as e:
                self.add_error("password1", e)
        return cleaned_data



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'image', 'birth_date']
        widgets = {
            'first_name': forms.TextInput(attrs={})
        }



# class EditUserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email']


