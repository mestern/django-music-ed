from django import forms

class TicketForm(forms.Form):
    SUBJECT_CHOICES=(
        ('suggestions', 'SUG'),
        ('criticism', 'CRT'),
        ('report', 'REP')
    )
    name = forms.CharField(max_length=50, required=True)
    subject = forms.CharField(choices=SUBJECT_CHOICES, required=True)
    phone = forms.CharField(max_length=11, required=True)
    email = forms.CharField(max_length=250, required=False)
    message = forms.CharField(widget=forms.Textarea, required=True)
