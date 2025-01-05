#first two things is import
from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TweetForm(forms.ModelForm):
    class Meta:
        model=Tweet
        # fields=['text','photo']
        fields=['document','preview_image', 'description','price','email','contact_number','status']
        widgets = {
            'description': forms.Textarea(attrs={
                'cols': 20,
                'rows': 10,
                'class': 'textarea'  # Add a custom class if needed for styling
            })
        }
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User

        fields=('username','email','password1','password2')
#edited part

    