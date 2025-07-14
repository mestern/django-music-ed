from django import forms
from django.shortcuts import get_object_or_404

from .models import Post, Comment
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
    publish = forms.DateTimeField()

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('Enter a Valid Phone Number')

        return phone


class PostCreateForm(forms.Form):
    auth = forms.CharField(max_length=50, required=True)
    image = forms.ImageField(required=False)
    title = forms.CharField(max_length=30, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    file = forms.FileField(required=False)

    def clean_auth(self):
        auth = self.cleaned_data['auth']
        if auth:
            try:
                User.objects.get(username=auth)
                return auth

            except:
                raise forms.ValidationError('Enter a Valid username')


class CommentFrom(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'message']
