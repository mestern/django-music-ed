from django import forms
from .models import Post

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


class PostCreateForm(forms.ModelForm):
    auth = forms.CharField(max_length=50, required=True)
    image = forms.ImageField(required=True)
    title = forms.CharField(max_length=30, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    publish = forms.CharField(max_length=50, required=True)
    class Meta:
        model = Post        # <--- This MUST be here
        fields = ['auth', 'title', 'image', 'description', 'slug']