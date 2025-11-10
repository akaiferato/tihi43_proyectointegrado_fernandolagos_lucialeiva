from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'telephone_number', 'area')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'telephone_number', 'area', 'observaciones', 'profile_picture')

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 2 * 1024 * 1024:
                raise ValidationError("La imagen no puede pesar mas de 2MB.")
            
            allowed_extensions = ['jpg', 'jpeg', 'png']
            extension = picture.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise ValidationError("Solo se permiten imagenes con extension .jpg, .jpeg o .png.")
        return picture

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups', 'is_staff', 'is_active', 'telephone_number', 'state', 'mfa_enabled', 'area', 'observaciones', 'profile_picture')
