from django import forms
from django.contrib import admin
from django.conf import settings
from .models import UserDevice
from cryptography.fernet import Fernet

cipher = Fernet(settings.ENCRYPTION_KEY)

class UserDeviceForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
    )

    class Meta:
        model = UserDevice
        fields = ['user', 'password', 'confirm_password', 'group']
        field_order = ['user', 'password', 'confirm_password', 'group']

    def clean(self):
        cleaned_data = super().clean()
        print("Cleaned data:", cleaned_data) 
        
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        encrypted_password = cipher.encrypt(password.encode())
        cleaned_data['password'] = encrypted_password.decode()

        return cleaned_data