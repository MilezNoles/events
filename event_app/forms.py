from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserLogin(AuthenticationForm):
    username = forms.CharField(label="Login",
                               widget=forms.TextInput(attrs={'class': "form-control",
                                                             "placeholder": "Username"}), )
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'class': "form-control", }))


class UserRegister(UserCreationForm):
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(attrs={'class': "form-control", }),
                               help_text="Mast be less than 150 chars")
    email = forms.EmailField(label="Email",
                             widget=forms.EmailInput(attrs={'class': "form-control", }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': "form-control", }),
                                help_text="Longer than 8 chars (letters & nums)")
    password2 = forms.CharField(label="Confirm password",
                                widget=forms.PasswordInput(attrs={'class': "form-control", }))
    is_event_creator = forms.BooleanField(label="Event manager", required=False,
                                          widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_event_creator",)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "city", "profile_picture", ]
        widgets = {"bio": forms.Textarea(attrs={'class': "form-control", }),
                   "city": forms.TextInput(attrs={'class': "form-control", "placeholder": "current city", }),
                   "profile_picture": forms.FileInput(attrs={'class': "form-control", }),

                   }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["content", ]
        widgets = {"content": forms.Textarea(attrs={'class': "form-control", }), }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ["content", "files", ]
        widgets = {"content": forms.Textarea(attrs={'class': "form-control", }),
                   "files": forms.FileInput(attrs={'class': "form-control", }),

                   }


class MyWidgetDateInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "event_type", "content", "city", "date"]
        widgets = {"title": forms.TextInput(attrs={'class': "form-control", }),
                   "event_type": forms.Select(attrs={'class': "form-control", }),
                   "content": forms.Textarea(attrs={'class': "form-control", }),
                   "city": forms.TextInput(attrs={'class': "form-control", }),
                   "date": MyWidgetDateInput(attrs={'class': "form-control", }),

                   }
