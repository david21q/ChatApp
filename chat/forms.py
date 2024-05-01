from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add an email field for user registration

    class Meta:
        model = User  # The form is based on the User model
        fields = ("username", "email", "password1", "password2")  # Specify form fields

    def save(self, commit=True):
        user = super().save(commit=False)  # Call the parent class's save method
        user.email = self.cleaned_data["email"]  # Save the email
        if commit:
            user.save()  # Save the user if commit is True
        return user


class ChangeUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]  # Only the username field

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username