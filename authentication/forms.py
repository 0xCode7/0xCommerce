from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from store.models import Profile


class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="Phone",
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
                            required=False)
    address1 = forms.CharField(label="Address1",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address1'}),
                               required=False)
    address2 = forms.CharField(label="Address2",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address2'}),
                               required=False)
    country = forms.CharField(label="Country",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
                              required=False)
    city = forms.CharField(label="City", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
                           required=False)
    state = forms.CharField(label="State", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
                            required=False)
    zipcode = forms.CharField(label="Zipcode",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
                              required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2', 'country', 'city', 'state', 'zipcode')


class UpdateUserForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Enter your first name")
    last_name = forms.CharField(max_length=30, required=True, help_text="Enter your last name")
    email = forms.EmailField(required=True, help_text="Enter a valid email address")
    password1 = forms.CharField(
        max_length=128, required=False, widget=forms.PasswordInput, help_text="Enter a new password (optional)"
    )
    password2 = forms.CharField(
        max_length=128, required=False, widget=forms.PasswordInput, help_text="Confirm the new password (optional)"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.email != email and User.objects.filter(email=email).exists():
            raise ValidationError("This email is already taken")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.username != username and User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:  # Check if either field is filled
            if password1 != password2:
                raise ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class SignInForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Enter your first name")
    last_name = forms.CharField(max_length=30, required=True, help_text="Enter your last name")
    email = forms.EmailField(required=True, help_text="Enter a valid email address")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already taken")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
