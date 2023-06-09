from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.hashers import make_password

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=User.ROLES, initial='student')
    bio = forms.CharField(max_length=500)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'bio']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user