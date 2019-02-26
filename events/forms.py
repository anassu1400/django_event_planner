from django import forms
from django.contrib.auth.models import User
from .models import EventModel, Booking

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }

class EventForm(forms.ModelForm):
	class Meta:
		model = EventModel
		exclude = ['organizer']
		widgets={
			'date': forms.DateInput(attrs={'type':'date'}),
			'time': forms.TimeInput(attrs={'type':'time'}),

		}

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats']
    

class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

