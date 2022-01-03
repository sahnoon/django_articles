from django import forms
from functools import partial
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

# TODO add dateinput and date picker in the html
DateInput = partial(
    forms.DateInput, {'class': 'datepicker', 'autocomplete': 'off', 'placeholder': 'YYYY-MM-DD'})

class SignUpForm(UserCreationForm):
    """To customize the sign up form

    Args:
        UserCreationForm (UserCreationForm): Django default user creation form
    """
    # failed to get user name
    username = forms.CharField(max_length=30)
    # email faild 
    email = forms.EmailField(max_length=200)
    # phone failed with minmum 9 digits and maxmum 15 digit all of them are numbers
    phone = forms.CharField(label='phone number', min_length=9, max_length=15,
                                   validators=[RegexValidator(
                                       r'^\+?1?\d{9,15}$')],
                                    widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    # id failed to get the national id
    id = forms.CharField(label='National ID', min_length=10, max_length=10,
                                   validators=[RegexValidator(
                                       r'^\+?1?\d{10,10}$')],
                                    widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    # date failed to get the date of birth 
    dob = forms.DateField(widget=DateInput(),
                                       label='Date of birth')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'id', 'dob')