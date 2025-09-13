# imports forms to make my forms
from django import forms
from django.shortcuts import get_object_or_404

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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=50, required=True)
