from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from reservation.models import Reservation


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")  # customer must enter email

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["name","table","reservation_date","reservation_time","guests"]

