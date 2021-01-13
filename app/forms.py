from django.shortcuts import render
from .models import vehicle, insurance
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from material import *


class SignUpForm(UserCreationForm):
    username = forms.CharField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(label="Email Address")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Enter password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    receive_news = forms.BooleanField(required=False, label='I want to receive news and notifications')
    agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')

    layout = Layout('username', 'email',
                    Row('password1', 'password2'),
                    Fieldset('Personal details',
                             Row('first_name', 'last_name'),
                             'receive_news', 'agree_toc'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class VehicleForm(forms.ModelForm):
    vehicle_name = forms.CharField()
    vehicle_number = forms.CharField()
    vehicle_reg_year = forms.DateField(label="Ex: 2017-01-30")
    vehicle_price = forms.IntegerField()
    insurance_name = forms.CharField(required=False)
    insurance_type = forms.IntegerField(required=False)
    insurance_price = forms.IntegerField(required=False)

    layout = Layout('vehicle_name',
                    Row('vehicle_number'),
                    Fieldset('Vehicle details',
                             Row('vehicle_reg_year', 'vehicle_price')))

    class Meta:
        model = vehicle
        fields = ('vehicle_name', 'vehicle_number', 'vehicle_reg_year', 'vehicle_price',)


class InsuranceForm(forms.ModelForm):
    insurance_name = forms.CharField()
    insurance_type = forms.IntegerField(label="Two or Four Wheeler")
    insurance_basic_price = forms.IntegerField()
    insurance_desc = forms.CharField()

    layout = Layout('insurance_name', 'insurance_type','insurance_desc',
                    Fieldset('Insurance details',
                             Row('insurance_basic_price')))

    class Meta:
        model = insurance
        fields = ('insurance_name', 'insurance_type', 'insurance_desc', 'insurance_basic_price',)
