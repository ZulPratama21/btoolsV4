from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from .models import UserDevice
from cryptography.fernet import Fernet

cipher = Fernet(settings.ENCRYPTION_KEY)

class UserDeviceForm(forms.ModelForm):
    user = forms.ChoiceField(
        initial='admin',
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].choices = [(user.username, user.first_name.capitalize()) for user in User.objects.all()]

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