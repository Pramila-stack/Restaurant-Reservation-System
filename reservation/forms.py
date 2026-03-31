from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from reservation.models import Reservation, Table


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
        fields = ['table', 'guests', 'reservation_date', 'reservation_time']
        widgets = {
            'reservation_time': forms.TimeInput(format='%H:%M', attrs={'type':'time'}),
            'reservation_date': forms.DateInput(attrs={'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        date = kwargs.pop('date', None)
        time = kwargs.pop('time', None)
        super().__init__(*args, **kwargs)

        if date and time:
            booked_tables = Reservation.objects.filter(
                reservation_date=date,
                reservation_time=time,
                status__in=['pending', 'confirmed']
            ).values_list('table_id', flat=True)

            # Only show available tables
            self.fields['table'].queryset = Table.objects.exclude(id__in=booked_tables)